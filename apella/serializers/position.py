from django.conf import settings
from django.utils import timezone
from rest_framework import serializers

from apella.serializers.mixins import ValidatorMixin
from apella.models import Position, InstitutionManager, Candidacy, \
    Professor, ElectorParticipation


def get_electors_regular_internal(instance):
    return Professor.objects.filter(
        electorparticipation__is_regular=True,
        electorparticipation__position_id=instance.id,
        registry__type=1,
        registry__department_id=instance.department.id).distinct()


def get_electors_regular_external(instance):
    return Professor.objects.filter(
        electorparticipation__is_regular=True,
        electorparticipation__position_id=instance.id,
        registry__type=2,
        registry__department_id=instance.department.id).distinct()


def get_electors_sub_internal(instance):
    return Professor.objects.filter(
        electorparticipation__is_regular=False,
        electorparticipation__position_id=instance.id,
        registry__type=1,
        registry__department_id=instance.department.id).distinct()


def get_electors_sub_external(instance):
    return Professor.objects.filter(
        electorparticipation__is_regular=False,
        electorparticipation__position_id=instance.id,
        registry__type=2,
        registry__department_id=instance.department.id).distinct()


def get_committee_internal(instance):
    return instance.committee.filter(
        registry__type=1,
        registry__department_id=instance.department.id).distinct()


def get_committee_external(instance):
    return instance.committee.filter(
        registry__type=2,
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
        committee = data.pop('committee', [])
        assistants = data.pop('assistants', [])
        ranks = data.pop('ranks', [])
        data = super(PositionMixin, self).validate(data)
        data['committee'] = committee
        data['assistants'] = assistants
        data['ranks'] = ranks

        return data

    def create(self, validated_data):
        validated_data['state'] = 'posted'
        validated_data['department_dep_number'] = \
            get_dep_number(validated_data)
        validated_data['author'] = get_author(self.context.get('request'))
        obj = super(PositionMixin, self).create(validated_data)
        code = settings.POSITION_CODE_PREFIX + str(obj.id)
        obj.code = code
        obj.save()
        return obj

    def update(self, instance, validated_data):
        curr_position = Position.objects.get(id=instance.id)
        assistants = curr_position.assistants.all()
        committee = curr_position.committee.all()
        ranks = curr_position.ranks.all()

        validated_data['updated_at'] = timezone.now()
        eps = curr_position.electorparticipation_set.all()

        instance = super(PositionMixin, self).update(instance, validated_data)
        if instance.state != curr_position.state:
            curr_position.pk = None
            curr_position.save()
            curr_position.assistants = assistants
            curr_position.committee = committee
            curr_position.ranks = ranks
            curr_position.save()
            for ep in eps:
                ElectorParticipation.objects.create(
                    position=curr_position,
                    professor=ep.professor,
                    is_regular=ep.is_regular)
        return instance


class CandidacyMixin(ValidatorMixin):

    def create(self, validated_data):
        user = self.context.get('request').user
        if not user.is_helpdesk():
            validated_data['candidate'] = user
        validated_data['state'] = 'posted'
        obj = super(CandidacyMixin, self).create(validated_data)
        code = str(obj.id)
        obj.code = code
        obj.save()
        return obj

    def update(self, instance, validated_data):
        curr_candidacy = Candidacy.objects.get(id=instance.id)
        validated_data['updated_at'] = timezone.now()
        instance = super(CandidacyMixin, self).update(instance, validated_data)
        if instance.state is not curr_candidacy.state:
            curr_candidacy.pk = None
            curr_candidacy.save()
        return instance
