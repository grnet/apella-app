from django.conf import settings
from django.utils import timezone
from rest_framework import serializers

from apella.serializers.mixins import ValidatorMixin
from apella.models import Position, InstitutionManager, Candidacy


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
        electors = data.pop('electors', [])
        assistants = data.pop('assistants', [])
        ranks = data.pop('ranks', [])
        data = super(PositionMixin, self).validate(data)
        data['committee'] = committee
        data['electors'] = electors
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
        electors = curr_position.electors.all()
        committee = curr_position.committee.all()
        ranks = curr_position.ranks.all()

        instance = super(PositionMixin, self).update(instance, validated_data)
        if instance.state != curr_position.state:
            curr_position.pk = None
            curr_position.save()
            curr_position.assistants = assistants
            curr_position.electors = electors
            curr_position.committee = committee
            curr_position.ranks = ranks
            curr_position.created_at = timezone.now()
            curr_position.save()
        return instance


class CandidacyMixin(ValidatorMixin):

    def create(self, validated_data):
        user = self.request.user
        if not user.is_helpdesk():
            validated_data['user'] = user
        validated_data['state'] = 'posted'
        obj = super(CandidacyMixin, self).create(validated_data)
        code = str(obj.id)
        obj.code = code
        obj.save()
        return obj

    def update(self, instance, validated_data):
        curr_candidacy = Candidacy.objects.get(id=instance.id)
        instance = super(CandidacyMixin, self).update(instance, validated_data)
        if instance.state is not curr_candidacy.state:
            curr_candidacy.pk = None
            curr_candidacy.submitted_at = timezone.now()
            curr_candidacy.save()
        return instance
