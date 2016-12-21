from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


def assistant_can_edit(position, user):
    return position.author.user == user or \
        position in user.institutionmanager.assistant_duty.all()


def position_is_latest(position):
    return position.code.split(settings.POSITION_CODE_PREFIX)[1] == \
        str(position.id)


def professor_participates(user, position_id):
    try:
        has_elector_duty = \
            user.professor.elector_duty.filter(id=position_id)
    except ObjectDoesNotExist:
        return False
    if has_elector_duty:
        return True
    has_committee_duty = \
        user.professor.committee_duty.filter(id=position_id)
    if has_committee_duty:
        return True
    return False
