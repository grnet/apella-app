#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import csv
import re
import logging
from datetime import datetime, timedelta
from time import strftime, gmtime

from django.conf import settings
from django.core.files import File
from django.db import transaction
from django.db.models import Min
from django.db.utils import IntegrityError
from rest_framework import serializers

from apella.serializers.mixins import ValidatorMixin
from apella.models import Position, InstitutionManager, Candidacy, \
    ElectorParticipation, ApellaFile, generate_filename, Institution, \
    Department, Professor, ApellaUser, Candidate, RegistryMembership
from apella.validators import validate_now_is_between_dates, \
    validate_candidate_files, validate_unique_candidacy, \
    after_today_validator, before_today_validator, \
    validate_position_committee, validate_position_electors, \
    validate_position_state, validate_tenure_candidacy, \
    validate_create_position_from_application, validate_subject_fields
from apella.serials import get_serial
from apella.emails import send_create_candidacy_emails, \
    send_remove_candidacy_emails, send_email_elected, send_emails_field, \
    send_emails_members_change, send_position_create_emails
from apella.util import at_day_end, at_day_start, otz, safe_path_join
from apella.common import RANKS, RANKS_EL_EN

logger = logging.getLogger(__name__)


def position_can_accept_candidacies(instance):
    positions = instance.position_set.order_by('-id')
    if len(positions) > 0:
        position = positions[0]
        if position.ends_at is None:
            return True
    return False

def get_position_state_from_application(instance):
    positions = instance.position_set.all()
    ids = positions.values('code').annotate(Min('id')). \
        values_list('id__min', flat=True)
    if positions:
        return positions.filter(id=max(ids))[0].state
    else:
        return None

def get_position_from_application(instance):
    positions = instance.position_set.all()
    ids = positions.values('code').annotate(Min('id')). \
        values_list('id__min', flat=True)
    if positions:
        return max(ids)
    else:
        return 0

def get_electors_regular_internal(instance):
    eps = instance.electorparticipation_set.filter(
        is_regular=True,
        is_internal=True)
    return [ep.professor for ep in eps]


def get_electors_regular_external(instance):
    eps = instance.electorparticipation_set.filter(
        is_regular=True,
        is_internal=False)
    return [ep.professor for ep in eps]


def get_electors_sub_internal(instance):
    eps = instance.electorparticipation_set.filter(
        is_regular=False,
        is_internal=True)
    return [ep.professor for ep in eps]


def get_electors_sub_external(instance):
    eps = instance.electorparticipation_set.filter(
        is_regular=False,
        is_internal=False)
    return [ep.professor for ep in eps]


def get_committee_internal(instance):
    internal = []
    committee = instance.committee.all()
    for professor in committee:
        if RegistryMembership.objects.filter(
                professor=professor,
                registry__department=instance.department,
                registry__type='internal').exists() or \
                professor.department and \
                professor.department is instance.department:
            internal.append(professor)

    return internal


def get_committee_external(instance):
    internal = get_committee_internal(instance)
    return [ext for ext in instance.committee.all() if ext not in internal]


def get_dep_number(data):
    dep_number = data['department'].dep_number
    if dep_number is None:
        raise serializers.ValidationError(
            {"dep_number":
                "You should first set DEP number for the department"})
    elif int(dep_number) < 0:
        raise serializers.ValidationError(
            {"dep_number":
                "DEP number for the department should be a positive number"})
    return dep_number


def get_author(request):
    try:
        manager = InstitutionManager.objects.get(user_id=request.user.id)
    except InstitutionManager.DoesNotExist:
        raise serializers.ValidationError(
            {"author": "Only Institution Managers can create new positions"})
    return manager


class PositionNonModel(ValidatorMixin):

    def validate(self, data):
        committee_external = data.get('committee_external', [])
        committee_internal = data.get('committee_internal', [])
        if committee_internal or committee_external:
            validate_position_committee(committee_internal, committee_external)

        r_i = data.get('electors_regular_internal', [])
        r_e = data.get('electors_regular_external', [])

        if r_i or r_e:
            dep_number = self.instance.department_dep_number
            validate_position_electors(r_i, r_e, dep_number)

        return data


class PositionMixin(ValidatorMixin):

    def validate(self, data):
        user = self.context.get('request').user

        committee = data.pop('committee', [])

        user_application = data.get('user_application', None)
        instance = getattr(self, 'instance')
        creating = False
        if not instance:
            creating = True
            validate_subject_fields(data)
            ranks = self.context.get('request').data.get('ranks', [])
            if not ranks:
                raise serializers.ValidationError('ranks.required')

        position_type = 'election'
        if user_application is not None:
            if creating:
                validate_create_position_from_application(user_application)
            position_type = user_application.app_type
            data['position_type'] = position_type

            if not user.is_helpdeskadmin() and position_type == 'election':
                if 'starts_at' in data:
                    after_today_validator(data['starts_at'])
                if 'fek_posted_at' in data:
                    before_today_validator(data['fek_posted_at'])

        data = super(PositionMixin, self).validate(data)
        if committee:
            data['committee'] = committee

        return data

    def _normalize_dates(self, validated_data):
        starts_at = validated_data.get('starts_at', None)
        if starts_at is not None:
            validated_data['starts_at'] = at_day_start(starts_at, otz)
        elif self.instance and not self.instance.is_election_type \
                and self.instance.starts_at is None:
            starts_at = datetime.utcnow()
            validated_data['starts_at'] = \
                at_day_start(starts_at, otz) - timedelta(days=1)

        ends_at = validated_data.get('ends_at', None)
        if ends_at is not None:
            validated_data['ends_at'] = at_day_end(ends_at, otz)

    def create(self, validated_data):
        ranks = self.context.get('request').data.get('ranks', [])
        validated_data['rank'] = ranks[0]
        ranks = ranks[1:]
        validated_data['state'] = 'posted'
        validated_data['department_dep_number'] = \
            get_dep_number(validated_data)

        self._normalize_dates(validated_data)

        validated_data['author'] = get_author(self.context.get('request'))
        obj = super(PositionMixin, self).create(validated_data)
        code = settings.POSITION_CODE_PREFIX + str(obj.id)
        obj.code = code
        obj.save()
        send_position_create_emails(obj)

        related_positions = [obj]
        for rank in ranks:
            p = Position.objects.create(**validated_data)
            p.code = settings.POSITION_CODE_PREFIX + str(p.id)
            p.rank = rank
            p.save()
            related_positions.append(p)
            send_position_create_emails(p)

        for p in related_positions:
            for r in related_positions:
                if p.id != r.id:
                    p.related_positions.add(r)
                p.save()
        return obj

    def update(self, instance, validated_data):
        curr_position = Position.objects.get(id=instance.id)
        dep_number = curr_position.department.dep_number
        if curr_position.department_dep_number == 0 and \
                dep_number is None and curr_position.state == 'electing':
            raise serializers.ValidationError(
                {"non_field_errors":
                    "You should first set DEP number for the department"})

        committee = curr_position.committee.all()
        assistant_files = curr_position.assistant_files.all()
        old_committee = [p for p in committee.all()]

        validated_data['updated_at'] = datetime.utcnow()
        eps = curr_position.electorparticipation_set.all()

        self._normalize_dates(validated_data)

        instance = super(PositionMixin, self).update(instance, validated_data)

        if instance.state != curr_position.state:
            curr_position.pk = None
            curr_position.save()
            curr_position.committee = committee
            curr_position.assistant_files = assistant_files
            curr_position.save()
            for ep in eps:
                ElectorParticipation.objects.create(
                    position=curr_position,
                    professor=ep.professor,
                    is_internal=ep.is_internal,
                    is_regular=ep.is_regular)

            if curr_position.state == 'revoked' and \
                    instance.state == 'electing':
                for ep in ElectorParticipation.objects.filter(position=instance):
                    ep.delete()
                for p in instance.committee.all():
                    instance.committee.remove(p)
                instance.committee_note = None
                instance.committee_proposal = None
                instance.committee_set_file = None
                instance.electors_meeting_date = None
                instance.electors_meeting_proposal = None
                instance.electors_meeting_to_set_committee_date = None
                instance.electors_set_file = None
                instance.revocation_decision = None
                instance.nomination_proceedings = None
                instance.proceedings_cover_letter = None
                instance.nomination_act = None
                instance.elected = None
                instance.second_best = None
                instance.save()


        # send email to elected
        if validated_data.get('elected', None):
            if curr_position.elected != validated_data['elected']:
                send_email_elected(instance, 'elected')

        # send email to second_best
        if validated_data.get('second_best', None):
            if curr_position.second_best != validated_data['second_best']:
                send_email_elected(instance, 'second_best')

        # send emails when electors_meeting_date is set/updated
        d1 = validated_data.get('electors_meeting_date', None)
        if d1 and curr_position.state != 'revoked' and \
                instance.state != 'cancelled':
            d1 = d1.date()
            if not curr_position.electors_meeting_date:
                send_emails_field(instance, 'electors_meeting_date')
            else:
                curr_date = curr_position.electors_meeting_date.date()
                if curr_date != d1:
                    send_emails_field(instance, 'electors_meeting_date', True)

        # send emails when electors_meeting_to_set_committee_date is
        # set/updated
        d2 = validated_data.get('electors_meeting_to_set_committee_date', None)
        if d2 and curr_position.state != 'revoked' \
                and instance.state != 'cancelled':
            d2 = d2.date()
            if not curr_position.electors_meeting_to_set_committee_date:
                send_emails_field(instance,
                        'electors_meeting_to_set_committee_date')
            else:
                curr_date = \
                    curr_position.electors_meeting_to_set_committee_date.date()
                if curr_date != d2:
                    send_emails_field(instance,
                            'electors_meeting_to_set_committee_date', True)

        if curr_position.state == 'electing':
            new_committee = [p for p in instance.committee.all()]
            send_emails_members_change(instance, 'committee', {'c': old_committee},
                {'c': new_committee})

        return instance


def link_single_file(existing_file, dest_obj, source='candidacy'):
    new_file = ApellaFile(
        id=get_serial('apella_file'),
        owner=existing_file.owner,
        source=source,
        file_kind=existing_file.file_kind,
        source_id=dest_obj.id,
        description=existing_file.description,
        updated_at=datetime.utcnow(),
        file_name=existing_file.file_name)

    new_name = generate_filename(new_file, new_file.file_name)
    new_path = safe_path_join(settings.MEDIA_ROOT, new_name)
    existing_path = existing_file.file_content.path
    try:
        os.link(existing_path, new_path)
    except OSError as e:
        logger.error('failed to link %s file: %s' % (e, source))
        raise
    new_file.file_content = new_path
    new_file.save()
    return new_file


def link_files(dest_obj, user, source='candidacy'):
    if user.is_professor():
        cv = user.professor.cv
        pubs_note = user.professor.pubs_note
        diplomas = user.professor.diplomas.all()
        publications = user.professor.publications.all()
    elif user.is_candidate():
        cv = user.candidate.cv
        pubs_note = user.candidate.pubs_note
        diplomas = user.candidate.diplomas.all()
        publications = user.candidate.publications.all()

    new_cv = link_single_file(cv, dest_obj, source=source)
    dest_obj.cv = new_cv

    if pubs_note:
        new_pubs_note = link_single_file(pubs_note, dest_obj, source=source)
        dest_obj.pubs_note = new_pubs_note
    else:
        dest_obj.pubs_note = None

    dest_obj.diplomas.all().delete()
    dest_obj.publications.all().delete()

    for diploma in diplomas:
        new_diploma = link_single_file(diploma, dest_obj, source=source)
        dest_obj.diplomas.add(new_diploma)
    for publication in publications:
        new_publication = link_single_file(publication, dest_obj, source=source)
        dest_obj.publications.add(new_publication)
    dest_obj.save()


class CandidacyMixin(object):
    def validate(self, data):
        user = self.context.get('request').user
        instance = getattr(self, 'instance')
        creating = False

        attachment_files = data.pop('attachment_files', [])
        diplomas = data.pop('diplomas', [])
        publications = data.pop('publications', [])
        if not instance:
            creating = True
            instance = Candidacy(**data)

        cancelling = 'state' in self.context.get('request').data and \
            self.context.get('request').data['state'] == 'cancelled'

        if not cancelling:
            position = instance.position
            candidate = instance.candidate
            if not user.is_helpdeskadmin():
                if data and position.is_election_type:
                    validate_now_is_between_dates(
                        position.starts_at, position.ends_at)
            if creating:
                validate_candidate_files(candidate)
                validate_unique_candidacy(position, candidate)
                validate_position_state(position)
                if position.is_tenure_type:
                    validate_tenure_candidacy(position, candidate)

        data = super(CandidacyMixin, self).validate(data)
        data['attachment_files'] = attachment_files
        data['diplomas'] = diplomas
        data['publications'] = publications

        return data

    def create(self, validated_data):
        user = self.context.get('request').user
        if not user.is_helpdesk():
            validated_data['candidate'] = user
        validated_data['state'] = 'draft'
        attachment_files = validated_data.pop('attachment_files', [])
        diplomas = validated_data.pop('diplomas', [])
        publications = validated_data.pop('publications', [])
        obj = super(CandidacyMixin, self).create(validated_data)
        code = str(obj.id)
        obj.code = code
        obj.save()
        try:
            link_files(obj, validated_data.get('candidate'))
        except IOError:
            obj.delete()
            raise serializers.ValidationError(
                {"non_field_errors": "Failed to copy candidacy files"})
        obj.state = 'posted'
        obj.save()
        send_create_candidacy_emails(obj)
        logger.info('successfully created candidacy %s for candidate %s' %
            (str(obj.id), str(obj.candidate.id)))

        position = validated_data.get('position', None)
        ends_at = validated_data.get('ends_at', None)
        if not position.is_election_type and ends_at is None:
            position.ends_at = \
                at_day_start(datetime.utcnow(), otz) - timedelta(hours=1)
            position.save()
        return obj

    def update(self, instance, validated_data):
        curr_candidacy = Candidacy.objects.get(id=instance.id)
        updated_at = datetime.utcnow()
        validated_data['updated_at'] = updated_at
        attachment_files = validated_data.pop('attachment_files', [])
        self_evaluation_report = validated_data.pop(
            'self_evaluation_report', [])
        statement_file = validated_data.pop('statement_file', [])
        cv = validated_data.pop('cv', [])
        pubs_note = validated_data.pop('pubs_note', [])
        diplomas = validated_data.pop('diplomas', [])
        publications = validated_data.pop('publications', [])
        instance = super(CandidacyMixin, self).update(instance, validated_data)
        if instance.state != curr_candidacy.state:
            curr_candidacy.pk = None
            curr_candidacy.updated_at = updated_at - timedelta(seconds=1)
            curr_candidacy.save()
            instance.old_candidacy_id = None
            instance.save()
        state = validated_data.get('state', None)
        if state == 'cancelled':
            send_remove_candidacy_emails(instance)
        return instance

@transaction.atomic
def upgrade_candidate_to_professor(
        user, department=None, rank=None,
        fek=None, discipline_text=None, discipline_in_fek=None):

    if not department:
        raise serializers.ValidationError(
            {"department": "department.required.error"})
    try:
        department = Department.objects.get(id=department)
    except Department.DoesNotExist:
        raise serializers.ValidationError(
            {"department": "department.required.error"})

    ranks = [r for r, val in RANKS]
    if not rank or rank not in ranks:
        raise serializers.ValidationError(
            {"rank": "rank.required.error"})
    if not fek:
        raise serializers.ValidationError(
            {"fek": "fek.required.error"})
    if not discipline_text:
        raise serializers.ValidationError(
            {"discipline_text": "discipline_text.required.error"})
    if discipline_in_fek is None:
        raise serializers.ValidationError(
            {"discipline_in_fek": "discipline_in_fek.required.error"})

    if department.institution.has_shibboleth:
        user.can_set_academic = True

    professor = Professor.objects.create(
        user=user,
        institution=department.institution,
        department=department,
        rank=rank,
        fek=fek,
        discipline_text=discipline_text,
        discipline_in_fek=discipline_in_fek,
        is_verified=True,
        verified_at=datetime.utcnow())
    logger.info('created new professor object for user %r' % user.id)
    cv = user.candidate.cv
    if not cv:
        raise serializers.ValidationError(
            {"cv": "missing.file"})

    cv.file_kind = 'cv_professor'
    cv_professor = link_single_file(cv, professor, source='profile')
    professor.cv_professor = cv_professor
    professor.save()
    user.role = 'candidate'
    link_files(professor, user, source='profile')
    professor.user.role = 'professor'
    professor.user.save()

    return professor

@transaction.atomic
def upgrade_candidates_to_professors(csv_file, owner):
    filename = 'upgradeCandidatesToProfessors_' + \
        strftime("%Y%m%d_%H%M%S", gmtime()) + ".csv"
    file_path = os.path.join(settings.MEDIA_ROOT, owner.username)
    if not os.path.isdir(file_path):
        os.makedirs(file_path)

    f = os.path.join(file_path, filename)
    with open(f, 'wb+') as destination:
        for chunk in csv_file.chunks():
            destination.write(chunk)

    csv_reader = csv.reader(csv_file)

    csv_iterator = iter(csv_reader)
    for header in csv_iterator:
        break
    else:
        raise serializers.ValidationError("no.csv.data")

    errors = []
    success = []
    try:
        for user_id, last_name, first_name, father_name, department_id, \
            email, rank, fek, fek_subject, subject_in_fek \
                in csv_iterator:

            try:
                user = ApellaUser.objects.get(id=user_id)
            except ApellaUser.DoesNotExist:
                msg = "User %s does not exist" % user_id
                errors.append(msg)
                continue

            try:
                canidate = Candidate.objects.get(user=user)
            except Candidate.DoesNotExist:
                msg = "User %s is not a candidate" % user_id
                errors.append(msg)
                continue

            p_rank = [v for k, v in RANKS_EL_EN.items() if k == rank.strip()]
            if not p_rank:
                msg = "Rank error: %s" % rank
                errors.append(msg)
                continue

            try:
                upgrade_candidate_to_professor(
                        user,
                        department=department_id,
                        rank=p_rank[0],
                        fek=fek,
                        discipline_text=fek_subject,
                        discipline_in_fek=bool(
                            re.match('true', subject_in_fek, re.I)))
            except serializers.ValidationError as ve:
                msg = "Failed to upgrade user %r: %s" % (user_id, ve)
                errors.append(msg)
                continue
            except OSError as ose:
                msg = "Failed to upgrade user %r: %s" % (user_id, ose)
                errors.append(msg)
                continue
            except IntegrityError:
                msg = "User %r is already a professor" % user_id
                errors.append(msg)
                continue

            success.append("Upgraded user %r" % user_id)
    except ValueError:
        msg = "Incorrect csv file format, error in line %r" % \
            csv_iterator.line_num
        errors.append(msg)

    logger.info(
        "Upgrade candidates to professors: failed: %r, succeeded %r" %
        (errors, success))
    return errors, success
