#! /usr/bin/python
# -*- encoding: utf-8 -*-
from datetime import datetime

from django.conf import settings
from django.db.models import Min
from rest_framework import serializers
from rest_framework.utils import model_meta
from rest_framework.serializers import ValidationError

from apella.models import ApellaUser, Institution, Department, \
    Position, Professor, InstitutionManager, JiraIssue, UserApplication
from apella import auth_hooks
from apella.util import move_to_timezone, otz
from apella.emails import send_user_email, send_create_application_emails
from apella.jira_wrapper import create_issue, update_issue
from apella.helpers import position_is_latest

def user_application_cannot_create_position(instance):
    """
    Returns true if there exists at least one not cancelled latest position
    with approved user_application whose user and app_type are the same as
    the instance application or user application is in pending state.
    """
    if instance.state == 'pending':
        return True

    approved_apps = UserApplication.objects.filter(
        user=instance.user,
        app_type=instance.app_type,
        state='approved'
    )
    positions = Position.objects.filter(
        user_application__in=approved_apps
    ).exclude(state='cancelled')
    latest_positions = [x for x in positions if position_is_latest(x)]
    return len(latest_positions)>0


class ValidatorMixin(object):

    def validate(self, data):
        instance = getattr(self, 'instance')
        if not instance:
            model = self.Meta.model
            instance = model(**data)
        else:
            for attr, val in data.items():
                setattr(instance, attr, val)
        instance.clean()
        return super(ValidatorMixin, self).validate(data)


def create_objects(model, fields, validated_data):
    """
    Recursively creates nested objects.
    """
    for field_name, field in fields.iteritems():
        if isinstance(field, serializers.BaseSerializer) \
                and field_name in validated_data:
            nested_data = validated_data.pop(field_name, None)
            nested_object = create_objects(
                field.Meta.model, field.get_fields(), nested_data)
            validated_data[field_name] = nested_object

    info = model_meta.get_field_info(model)
    many_to_many = {}
    for field_name, relation_info in info.relations.items():
        if relation_info.to_many and (field_name in validated_data):
            many_to_many[field_name] = validated_data.pop(field_name)

    if model == ApellaUser:
        obj = model.objects.create_user(**validated_data)
    else:
        obj = model.objects.create(**validated_data)

    if many_to_many:
        for field_name, value in many_to_many.items():
            setattr(obj, field_name, value)
        obj.save()
    return obj


def update_objects(fields, validated_data, instance=None, model=None):
    """
    Recursively updated nested objects.
    """
    if not instance:
        return create_objects(model, fields, validated_data)
    info = model_meta.get_field_info(type(instance))
    many_to_many = {}
    for field_name, relation_info in info.relations.items():
        if relation_info.to_many and (field_name in validated_data):
            many_to_many[field_name] = validated_data.pop(field_name)

    for field_name, field in fields.iteritems():
        if isinstance(field, serializers.BaseSerializer) \
                and field_name in validated_data:
            nested_data = validated_data.pop(field_name, None)
            nested_object = update_objects(
                field.get_fields(), nested_data,
                instance=getattr(instance, field_name), model=field.Meta.model)
            setattr(instance, field_name, nested_object)
        elif field_name in validated_data:
            if field_name == 'password':
                continue
            else:
                setattr(instance, field_name, validated_data.get(field_name))
    if many_to_many:
        for field_name_many, value in many_to_many.items():
            setattr(instance, field_name_many, value)
    instance.save()
    return instance


class NestedWritableObjectsMixin(object):

    NESTED_USER_KEY = 'user'

    def __init__(self, *args, **kwargs):
        super(NestedWritableObjectsMixin, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and \
                request.method in ['GET', 'PUT', 'PATCH'] and \
                self.NESTED_USER_KEY in self.fields:
            self.fields[self.NESTED_USER_KEY].fields['username'].read_only = \
                True
            self.fields[self.NESTED_USER_KEY].fields['email'].read_only = \
                True
            del self.fields[self.NESTED_USER_KEY].fields['password']

    def create(self, validated_data):
        model = self.Meta.model
        obj = create_objects(model, self.get_fields(), validated_data)
        return obj

    def update(self, instance, validated_data):
        instance = update_objects(
            self.get_fields(), validated_data, instance=instance)
        if isinstance(instance, Department):
            empty_positions = Position.objects.filter(
                department=instance.id, department_dep_number=0)
            dep_number = validated_data.get('dep_number', 0)
            for p in empty_positions:
                if dep_number > 0:
                    p.department_dep_number = dep_number
                    p.save()
        return instance


class HelpdeskUsers(object):

    def to_representation(self, obj):
        data = super(HelpdeskUsers, self).to_representation(obj)
        if (obj.is_helpdesk() or obj.is_ministry()) and \
                self.context['view'].get_view_name() == 'Custom User':
            data = {'user': data}
        return data

    def to_internal_value(self, data):
        user = self.context.get('request').user
        if (user.is_helpdesk() or user.is_ministry()) and \
                self.context['view'].get_view_name() == 'Custom User':
            return self.context.get('request').data.get('user')
        return super(HelpdeskUsers, self).to_internal_value(data)


class Assistants(NestedWritableObjectsMixin):

    def create(self, validated_data):
        user = self.context.get('request').user
        if user.is_institutionmanager():
            validated_data['institution'] = user.institutionmanager.institution
        validated_data['user']['role'] = 'assistant'
        assistant = super(Assistants, self).create(validated_data)
        auth_hooks.verify_email(assistant.user)
        assistant.user.save()
        auth_hooks.verify_user(assistant)
        assistant.save()
        return assistant


SHIBBOLETH_IDP_WHITELIST = getattr(settings, 'SHIBBOLETH_IDP_WHITELIST', [])
class Professors(object):

    def validate_institution(self, value):
        user = self.instance and self.instance.user
        if user and user.shibboleth_idp and \
                not user.shibboleth_idp in SHIBBOLETH_IDP_WHITELIST:
            if not value or (value.idp != user.shibboleth_idp):
                raise ValidationError("invalid.institution")

        if user.shibboleth_idp:
            idp = user.shibboleth_idp
            org = user.shibboleth_schac_home_organization
            insts = Institution.objects.filter(idp=idp)
            if insts.count() > 1:
                if user.shibboleth_schac_home_organization:
                    insts = insts.filter(schac_home_organization=org)
                    if not value in insts:
                        raise ValidationError("invalid.institution")
        return value


def send_registry_emails(members, department):
    department_title_el = department.title.el
    department_title_en = department.title.en
    institution_title_el = department.institution.title.el
    institution_title_en = department.institution.title.en

    for professor in members:
        send_user_email(
            professor.user,
            'apella/emails/registry_add_member_to_member_subject.txt',
            'apella/emails/registry_add_member_to_member_body.txt',
            extra_context={
                'department_title_el': department_title_el,
                'department_title_en': department_title_en,
                'institution_title_el': institution_title_el,
                'institution_title_en': institution_title_en
            }
        )


class Registries(object):
    def create(self, validated_data):
        members = validated_data.get('members', [])
        department = validated_data.get('department', None)
        registry = super(Registries, self).create(validated_data)
        send_registry_emails(members, department)
        return registry

    def update(self, instance, validated_data):
        department = validated_data.get('department', instance.department)
        members_before = instance.members.all()
        members_after = validated_data.get('members', [])
        members_to_send = [
            member for member in members_after if member not in members_before]
        instance = super(Registries, self).update(instance, validated_data)
        send_registry_emails(members_to_send, department)
        return instance


class PositionsPortal(object):
    def to_representation(self, obj):
        now = move_to_timezone(datetime.utcnow(), otz)
        starts_at = None
        if obj.starts_at:
            starts_at = move_to_timezone(obj.starts_at, otz)
        ends_at = None
        if obj.ends_at:
            ends_at = move_to_timezone(obj.ends_at, otz)

        state_el = ''
        if obj.state == 'posted' and starts_at < now:
            state_el = u'Ανοιχτή'
        elif obj.state == 'posted' and starts_at >= now:
            state_el = u'Ενταγμένη'

        data = {
                'id': obj.code,
                'name': obj.title,
                'description': obj.description,
                'department': {
                    'id': obj.department.id,
                    'name': {
                        'el': obj.department.title.el,
                        'en': obj.department.title.en
                    },
                    'school': {
                        'id': obj.department.school.id,
                        'name': {
                            'el': obj.department.school.title.el,
                            'en': obj.department.school.title.en
                        },
                        'institution': {
                            'id': obj.department.institution.id,
                            'name': {
                                'el': obj.department.institution.title.el,
                                'en': obj.department.institution.title.en
                            },
                            'schacHomeOrganization':
                                obj.department.institution.schac_home_organization,
                            'category': obj.department.institution.category
                        }
                    }
                },
                'subject': {
                    'name': obj.discipline
                },
                'sector': {
                    'areaId': obj.subject_area.id,
                    'subjectId': obj.subject.id,
                    'name': {
                        'el': {
                            'area': obj.subject_area.title.el,
                            'subject': obj.subject.title.el
                        },
                        'en': {
                            'area': obj.subject_area.title.en,
                            'subject': obj.subject.title.en
                        }
                    }
                },
                'fek': obj.fek,
                'phase': {
                    'status': obj.state,
                    'clientStatusInGreek': state_el,
                    'clientStatus': obj.state,
                    'candidacies': {
                        'openingDate': starts_at and starts_at.date(),
                        'closingDate': ends_at and ends_at.date(),
                        'createdAt': obj.created_at and obj.created_at.date(),
                        'updatedAt': obj.updated_at and obj.updated_at.date()
                    },
                    'createdAt': obj.created_at and obj.created_at.date(),
                    'updatedAt': obj.updated_at and obj.updated_at.date()
                },
                'fekSentDate': obj.fek_posted_at and obj.fek_posted_at.date()
        }
        return data


class UserApplications(object):
    def validate(self, data):
        app_type = self.instance and self.instace.app_type \
            or data.get('app_type')
        user = data.get('user', None)
        if not user:
            user = self.context.get('request').user
        if UserApplication.objects.filter(
                user=user,
                app_type=app_type,
                state='pending').exists():
            raise ValidationError('cannot.create.application')

        approved_apps = UserApplication.objects.filter(
            user=user,
            app_type=app_type,
            state='approved')
        for app in approved_apps:
            positions = app.position_set.all()
            for p in positions:
                if p.state != 'cancelled' and position_is_latest(p):
                    raise ValidationError('cannot.create.application')
        return super(UserApplications, self).validate(data)

    def create(self, validated_data):
        user = validated_data.get('user', None)
        if not user:
            user = self.context.get('request').user
            validated_data['user'] = user
        try:
            department = user.professor.department
            validated_data['department'] = department
        except Professor.DoesNotExist:
            raise ValidationError("user.not.a.professor")
        except Department.DoesNotExist:
            raise ValidationError("invalid.department")

        obj = super(UserApplications, self).create(validated_data)
        send_create_application_emails(obj)
        return obj

    def update(self, instance, validated_data):
        validated_data['updated_at'] = datetime.utcnow()
        return super(UserApplications, self).update(instance, validated_data)


class InstitutionManagersMixin(object):
    def validate(self, data):
        instance = self.instance
        curr_institution = instance and instance.institution
        new_institution = data.get('institution', None)
        manager_exists = new_institution and \
                InstitutionManager.objects.filter(
                    manager_role='institutionmanager',
                    is_verified=True,
                    institution=new_institution).exists()

        msg = 'manager.exists'
        if instance:
            if new_institution.id != curr_institution.id and \
                    manager_exists:
                raise ValidationError(msg)
        else:
            if manager_exists:
                raise ValidationError(msg)

        return data


class JiraIssues(object):
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if isinstance(instance, JiraIssue):
            update_issue(instance)
        elif instance:
            for i in instance:
                update_issue(i)
        return super(JiraIssues, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        jira_issue = JiraIssue(**validated_data)
        new_issue = create_issue(jira_issue)
        validated_data['issue_key'] = new_issue.key
        return super(JiraIssues, self).create(validated_data)


def get_professor_registries(instance):
    active_registries = []
    registries = instance.registry_set.all()
    electors_positions = instance.electorparticipation_set.values(
        'position__code').annotate(Min('position_id')).values_list(
        'position_id__min', flat=True)
    committee_positions = instance.committee_duty.values(
        'code').annotate(Min('id')).values_list(
        'id__min', flat=True)
    for r in registries:
        if electors_positions.filter(
                position__state__in=['electing', 'revoked'],
                position__department=r.department).exists() or \
                committee_positions.filter(
                    state__in=['electing', 'revoked'],
                    department=r.department).exists():
            active_registries.append(r.id)
    return active_registries
