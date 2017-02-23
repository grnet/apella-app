from datetime import datetime

from django.conf import settings
from django.core.files import File
from rest_framework import serializers

from django.db.models import Q, Max
from apella.serializers.mixins import ValidatorMixin
from apella.models import Position, InstitutionManager, Candidacy, \
    Professor, ElectorParticipation, ApellaFile
from apella.validators import validate_position_dates, \
    validate_candidate_files, validate_unique_candidacy, \
    after_today_validator, before_today_validator
from apella.serials import get_serial
from apella.emails import send_user_email
from apella.util import move_to_timezone, strip_timezone, otz


def get_electors_regular_internal(instance):
    return Professor.objects.filter(
        electorparticipation__is_regular=True,
        electorparticipation__position_id=instance.id,
        registry__type='internal',
        registry__department_id=instance.department.id).distinct()


def get_electors_regular_external(instance):
    return Professor.objects.filter(
        electorparticipation__is_regular=True,
        electorparticipation__position_id=instance.id,
        registry__type='external',
        registry__department_id=instance.department.id).distinct()


def get_electors_sub_internal(instance):
    return Professor.objects.filter(
        electorparticipation__is_regular=False,
        electorparticipation__position_id=instance.id,
        registry__type='internal',
        registry__department_id=instance.department.id).distinct()


def get_electors_sub_external(instance):
    return Professor.objects.filter(
        electorparticipation__is_regular=False,
        electorparticipation__position_id=instance.id,
        registry__type='external',
        registry__department_id=instance.department.id).distinct()


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
                "You should first set DEP number for Department: %s"
                % data['department'].title.en})
    elif int(dep_number) <= 0:
        raise serializers.ValidationError(
            {"dep_number":
                "DEP number for Department should be a positive number: %s"
                % data['department'].title.en})
    return dep_number


def get_author(request):
    try:
        manager = InstitutionManager.objects.get(user_id=request.user.id)
    except InstitutionManager.DoesNotExist:
        raise serializers.ValidationError(
            {"author": "Only Institution Managers can create new positions"})
    return manager


class PositionMixin(ValidatorMixin):

    def validate(self, data):
        user = self.context.get('request').user

        committee = data.pop('committee', [])
        ranks = data.pop('ranks', [])

        if not user.is_helpdeskadmin():
            #if 'starts_at' in data:
                #after_today_validator(data['starts_at'])
            if 'fek_posted_at' in data:
                before_today_validator(data['fek_posted_at'])

        data = super(PositionMixin, self).validate(data)
        data['committee'] = committee
        data['ranks'] = ranks

        return data

    def create(self, validated_data):
        validated_data['state'] = 'posted'
        validated_data['department_dep_number'] = \
            get_dep_number(validated_data)
        starts_at = validated_data['starts_at']
        starts_at = move_to_timezone(starts_at, otz)
        starts_at = starts_at.replace(
            hour=0, minute=0, second=0, microsecond=0)
        starts_at = strip_timezone(starts_at)
        validated_data['starts_at'] = starts_at
        ends_at = validated_data['ends_at']
        ends_at = move_to_timezone(ends_at, otz)
        ends_at = ends_at.replace(
            hour=23, minute=59, second=59, microsecond=59)
        ends_at = strip_timezone(ends_at)
        validated_data['ends_at'] = ends_at

        validated_data['author'] = get_author(self.context.get('request'))
        obj = super(PositionMixin, self).create(validated_data)
        code = settings.POSITION_CODE_PREFIX + str(obj.id)
        obj.code = code
        obj.save()
        return obj

    def update(self, instance, validated_data):
        curr_position = Position.objects.get(id=instance.id)
        committee = curr_position.committee.all()
        ranks = curr_position.ranks.all()

        validated_data['updated_at'] = datetime.utcnow()
        eps = curr_position.electorparticipation_set.all()

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
        return instance


def copy_single_file(existing_file, candidacy, source='candidacy'):
    new_file = ApellaFile(
        id=get_serial('apella_file'),
        owner=existing_file.owner,
        source=source,
        file_kind=existing_file.file_kind,
        source_id=candidacy.id,
        description=existing_file.description,
        updated_at=datetime.utcnow(),
        file_name=existing_file.file_name)
    with open(existing_file.file_content.path, 'r') as f:
        new_file.file_content.save(existing_file.file_name, File(f))
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
        copy_candidacy_files(obj, validated_data.get('candidate'))
        obj.state = 'posted'
        obj.save()
        send_create_candidacy_emails(obj)
        return obj



    def update(self, instance, validated_data):
        curr_candidacy = Candidacy.objects.get(id=instance.id)
        validated_data['updated_at'] = datetime.utcnow()
        attachment_files = validated_data.pop('attachment_files', [])
        self_evaluation_report = validated_data.pop(
            'self_evaluation_report', [])
        cv = validated_data.pop('cv', [])
        diplomas = validated_data.pop('diplomas', [])
        publications = validated_data.pop('publications', [])
        instance = super(CandidacyMixin, self).update(instance, validated_data)
        if instance.state is not curr_candidacy.state:
            curr_candidacy.pk = None
            curr_candidacy.save()
        state = validated_data['state']
        if state == 'cancelled':
            send_remove_candidacy_emails(instance)
        return instance


def send_create_candidacy_emails(candidacy):
    # send to candidate
    send_user_email(
        candidacy.candidate,
        'apella/emails/candidacy_create_subject.txt',
        'apella/emails/candidacy_create_to_candidate_body.txt',
        { 'position': candidacy.position })

    # send to managers
    recipients = candidacy.position.department.institution.\
        institutionmanager_set.all().filter(manager_role='institutionmanager')
    for recipient in recipients:
        send_user_email(
            recipient.user,
            'apella/emails/candidacy_create_subject.txt',
            'apella/emails/candidacy_create_to_manager_body.txt',
            {
                'position': candidacy.position,
                'candidate': candidacy.candidate
            })

    # send to secretaries
    recipients = candidacy.position.department.\
        institutionmanager_set.all().filter(is_secretary=True)
    for recipient in recipients:
        send_user_email(
            recipient.user,
            'apella/emails/candidacy_create_subject.txt',
            'apella/emails/candidacy_create_to_manager_body.txt',
            {
                'position': candidacy.position,
                'candidate': candidacy.candidate
            })


def send_remove_candidacy_emails(candidacy):
    # send to candidate
    send_user_email(
        candidacy.candidate,
        'apella/emails/candidacy_remove_subject.txt',
        'apella/emails/candidacy_remove_to_candidate_body.txt',
        { 'position': candidacy.position })

    # send to managers
    recipients = candidacy.position.department.institution.\
        institutionmanager_set.all().filter(manager_role='institutionmanager')
    for recipient in recipients:
        send_user_email(
            recipient.user,
            'apella/emails/candidacy_remove_subject.txt',
            'apella/emails/candidacy_remove_to_manager_body.txt',
            {
                'position': candidacy.position,
                'candidate': candidacy.candidate
            })

    # send to secretaries
    recipients = candidacy.position.department.\
        institutionmanager_set.all().filter(is_secretary=True)
    for recipient in recipients:
        send_user_email(
            recipient.user,
            'apella/emails/candidacy_remove_subject.txt',
            'apella/emails/candidacy_remove_to_manager_body.txt',
            {
                'position': candidacy.position,
                'candidate': candidacy.candidate
            })

    # send to electors
    recipients = candidacy.position.electors.all()
    for recipient in recipients:
        send_user_email(
            recipient.user,
            'apella/emails/candidacy_remove_subject.txt',
            'apella/emails/candidacy_remove_to_elector_body.txt',
            {
                'position': candidacy.position,
                'candidate': candidacy.candidate
            })

    # send to committee
    recipients = candidacy.position.committee.all()
    for recipient in recipients:
        send_user_email(
            recipient.user,
            'apella/emails/candidacy_remove_subject.txt',
            'apella/emails/candidacy_remove_to_committee_body.txt',
            {
                'position': candidacy.position,
                'candidate': candidacy.candidate
            })

    # send to cocandidates
    c_set = candidacy.position.candidacy_set.all()
    updated = c_set.values('candidate').annotate(Max('updated_at')).\
            values('updated_at__max')
    candidacies = c_set.filter(Q(updated_at__in=updated) & Q(state='posted'))

    for r in candidacies:
        recipient = r.candidate
        send_user_email(
            recipient,
            'apella/emails/candidacy_remove_subject.txt',
            'apella/emails/candidacy_remove_to_cocandidate_body.txt',
            {
                'position': candidacy.position,
                'candidate': candidacy.candidate
            })
