from django.conf import settings
from rest_framework import serializers
from rest_framework.utils import model_meta
from rest_framework.serializers import ValidationError

from apella.models import ApellaUser, Position, InstitutionManager, Institution
from apella import auth_hooks


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
            self.fields[self.NESTED_USER_KEY].fields['email'].read_only = \
                True
            self.fields[self.NESTED_USER_KEY].fields['username'].read_only = \
                True
            del self.fields[self.NESTED_USER_KEY].fields['password']

    def create(self, validated_data):
        model = self.Meta.model
        obj = create_objects(model, self.get_fields(), validated_data)
        return obj

    def update(self, instance, validated_data):
        instance = update_objects(
            self.get_fields(), validated_data, instance=instance)
        return instance


class HelpdeskUsers(object):

    def to_representation(self, obj):
        data = super(HelpdeskUsers, self).to_representation(obj)
        if obj.is_helpdesk() and \
                self.context['view'].get_view_name() == 'Custom User':
            data = {'user': data}
        return data

    def to_internal_value(self, data):
        user = self.context.get('request').user
        request_data = self.context.get('request').data
        if user.is_helpdesk() and \
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


class Professors(object):

    def validate_institution(self, value):
        user = self.instance and self.instance.user
        if user and user.shibboleth_idp:
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
