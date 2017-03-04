import logging
from datetime import datetime, timedelta

from django.conf import settings
from django.core.files import File
from rest_framework import serializers

from apella.serializers.mixins import ValidatorMixin
from apella.models import Position, InstitutionManager, Candidacy, \
    ElectorParticipation, ApellaFile
from apella.validators import validate_position_dates, \
    validate_candidate_files, validate_unique_candidacy, \
    after_today_validator, before_today_validator, \
    validate_position_committee, validate_position_electors
from apella.serials import get_serial
from apella.emails import send_create_candidacy_emails, \
    send_remove_candidacy_emails, send_email_elected, send_emails_field, \
    send_emails_members_change, send_position_create_emails
from apella.util import at_day_end, at_day_start, otz

logger = logging.getLogger(__name__)

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
    return instance.committee.filter(
        registry__type='internal',
        registry__department_id=instance.department.id).distinct()


def get_committee_external(instance):
    return instance.committee.filter(
        registry__type='external',
        registry__department_id=instance.department.id).distinct()


def get_dep_number(data):
    dep_number = data['department'].dep_number
    if dep_number is None:
        raise serializers.ValidationError(
            {"dep_number":
                "You should first set DEP number for the department"})
    elif int(dep_number) <= 0:
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
        s_i = data.get('electors_sub_internal', [])
        s_e = data.get('electors_sub_external', [])

        if r_i or r_e or s_i or s_e:
            dep_number = self.instance.department_dep_number
            validate_position_electors(r_i, r_e, s_i, s_e, dep_number)

        return data


class PositionMixin(ValidatorMixin):

    def validate(self, data):
        user = self.context.get('request').user

        committee = data.pop('committee', [])
        ranks = data.pop('ranks', [])

        if not user.is_helpdeskadmin():
            if 'starts_at' in data:
                after_today_validator(data['starts_at'])
            if 'fek_posted_at' in data:
                before_today_validator(data['fek_posted_at'])

        data = super(PositionMixin, self).validate(data)
        data['committee'] = committee
        data['ranks'] = ranks

        return data

    def _normalize_dates(self, validated_data):
        starts_at = validated_data.get('starts_at', None)
        if starts_at is not None:
            validated_data['starts_at'] = at_day_start(starts_at, otz)

        ends_at = validated_data.get('ends_at', None)
        if ends_at is not None:
            validated_data['ends_at'] = at_day_end(ends_at, otz)

    def create(self, validated_data):
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
        return obj

    def update(self, instance, validated_data):
        curr_position = Position.objects.get(id=instance.id)
        committee = curr_position.committee.all()
        old_committee = [p for p in committee.all()]
        ranks = curr_position.ranks.all()

        validated_data['updated_at'] = datetime.utcnow()
        eps = curr_position.electorparticipation_set.all()

        self._normalize_dates(validated_data)

        instance = super(PositionMixin, self).update(instance, validated_data)

        if instance.state != curr_position.state:
            curr_position.pk = None
            curr_position.save()
            curr_position.committee = committee
            curr_position.ranks = ranks
            curr_position.save()
            for ep in eps:
                ElectorParticipation.objects.create(
                    position=curr_position,
                    professor=ep.professor,
                    is_regular=ep.is_regular)

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
        if d1:
            if not curr_position.electors_meeting_date:
                send_emails_field(instance, 'electors_meeting_date')
            else:
                if curr_position.electors_meeting_date != d1:
                    send_emails_field(instance, 'electors_meeting_date', True)

        # send emails when electors_meeting_to_set_committee_date is
        # set/updated
        d2 = validated_data.get('electors_meeting_to_set_committee_date', None)
        if d2:
            if not curr_position.electors_meeting_to_set_committee_date:
                send_emails_field(instance,
                        'electors_meeting_to_set_committee_date')
            else:
                if curr_position.electors_meeting_to_set_committee_date != d2:
                    send_emails_field(instance,
                            'electors_meeting_to_set_committee_date', True)

        new_committee = [p for p in instance.committee.all()]

        send_emails_members_change(instance, 'committee', {'c': old_committee},
            {'c': new_committee})

        return instance


def copy_single_file(existing_file, candidacy, source='candidacy'):
    new_file = ApellaFile(
        id=get_serial('apella_file'),
        owner=existing_file.owner,

        source_id=candidacy.id,
        description=existing_file.description,
        updated_at=datetime.utcnow(),
        file_name=existing_file.file_name)
    try:
        with open(existing_file.file_content.path, 'r') as f:
            new_file.file_content.save(existing_file.file_name, File(f))
    except IOError as e:
        logger.error('failed to copy candidacy file: %s' % e)
        raise
    return new_file


def copy_candidacy_files(candidacy, user):
    if user.is_professor():
        cv = user.professor.cv
        diplomas = user.professor.diplomas.all()
        publications = user.professor.publications.all()
    elif user.is_candidate():
        cv = user.candidate.cv
        diplomas = user.candidate.diplomas.all()
        publications = user.candidate.publications.all()

    new_cv = copy_single_file(cv, candidacy)
    candidacy.cv = new_cv

    candidacy.diplomas.all().delete()
    candidacy.publications.all().delete()

    for diploma in diplomas:
        new_diploma = copy_single_file(diploma, candidacy)
        candidacy.diplomas.add(new_diploma)
    for publication in publications:
        new_publication = copy_single_file(publication, candidacy)
        candidacy.publications.add(new_publication)
    candidacy.save()


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
                validate_position_dates(position.starts_at, position.ends_at)
            if creating:
                validate_candidate_files(candidate)
                validate_unique_candidacy(position, candidate)

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
            copy_candidacy_files(obj, validated_data.get('candidate'))
        except IOError:
            obj.delete()
            raise serializers.ValidationError(
                {"non_field_errors": "Failed to copy candidacy files"})
        obj.state = 'posted'
        obj.save()
        send_create_candidacy_emails(obj)
        logger.info('successfully created candidacy %s for candidate %s' %
            (str(obj.id), str(obj.candidate.id)))
        return obj

    def update(self, instance, validated_data):
        curr_candidacy = Candidacy.objects.get(id=instance.id)
        updated_at = datetime.utcnow()
        validated_data['updated_at'] = updated_at
        attachment_files = validated_data.pop('attachment_files', [])
        self_evaluation_report = validated_data.pop(
            'self_evaluation_report', [])
        cv = validated_data.pop('cv', [])
        diplomas = validated_data.pop('diplomas', [])
        publications = validated_data.pop('publications', [])
        instance = super(CandidacyMixin, self).update(instance, validated_data)
        if instance.state is not curr_candidacy.state:
            curr_candidacy.pk = None
            curr_candidacy.updated_at = updated_at - timedelta(seconds=1)
            curr_candidacy.save()
            instance.old_candidacy_id = None
            instance.save()
        state = validated_data['state']
        if state == 'cancelled':
            send_remove_candidacy_emails(instance)
        return instance
