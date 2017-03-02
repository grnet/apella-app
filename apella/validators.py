from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from apella.util import strip_timezone, get_today_start, get_today_end, \
    at_day_start, at_day_end, otz


def before_today_validator(value):
    value = strip_timezone(value)
    today_start = get_today_start()
    if type(value) is date:
        today_start = today_start.date()
    if not value or value >= today_start:
        raise ValidationError(_('Date should be before today'))


def after_today_validator(value):
    value = strip_timezone(value)
    today_end = get_today_end()
    if type(value) is date:
        today_end = today_end.date()
    if not value or value < today_end:
        raise ValidationError(_('Date should be after today'))


def validate_dates_interval(start, end, interval):
    start = at_day_start(start, otz)
    end = at_day_end(end, otz)
    t = timedelta(days=interval) - timedelta(hours=1, seconds=1)
    if end - start <= t:
        raise ValidationError(
            _('End date should be %s days after start date' % interval))


def validate_position_dates(start, end):
    start = strip_timezone(start)
    end = strip_timezone(end)
    today_start = get_today_start()
    if today_start < start:
        raise ValidationError(_('Position opens at %s' % start))
    if today_start > end:
        raise ValidationError(_('Position closed at %s' % end))


def validate_candidate_files(user):
    if user.is_candidate():
        cv = user.candidate.cv
        diplomas = user.candidate.diplomas.all()
        publications = user.candidate.publications.all()
    elif user.is_professor():
        cv = user.professor.cv
        diplomas = user.professor.diplomas.all()
        publications = user.professor.publications.all()

    if not cv:
        raise ValidationError(
            _('You should upload a CV file to your profile '
                'before submitting a candidacy'))
    if not diplomas:
        raise ValidationError(
            _('You should upload a diploma file to your profile '
                'before submitting a candidacy'))
    if not publications:
        raise ValidationError(
            _('You should upload a publication file to your profile '
                'before submitting a candidacy'))


def validate_unique_candidacy(position, user):
    c_ids = user.candidacy_set.filter(
        state='posted', position=position).values_list('id', flat=True)
    c_codes = user.candidacy_set.filter(
        state='posted', position=position).values_list('code', flat=True)
    c_codes = map(int, c_codes)

    if filter(lambda x: x in c_ids, c_codes):
        raise ValidationError(
            _('You have already submitted a candidacy for this '
                'position'))


def validate_position_committee(internal, external):
    if len(external) < 1:
        raise ValidationError(
            _('At least one member of the committee must be '
                'from the external registry'))
    if (len(external) + len(internal)) != 3:
        raise ValidationError(
            _('The committee must contain exactly 3 members'))


def validate_position_electors(r_i, r_e, s_i, s_e, dep_number):
    """
    If dep_number is more than 40, electors should be exactly 15 regular and
    15 substitute members.
    If dep_number is less than or equal to 40, electors should be exactly 11
    regular and 11 substitute members

    r_i: electors_regular_internal
    r_e: electors_regular_external
    s_i: electors_sub_internal
    s_e: electors_sub_external
    """

    regular = len(r_i) + len(r_e)
    sub = len(s_i) + len(s_e)
    if dep_number > 40:
        if regular != 15:
            raise ValidationError(
                _('Regular electors must be exactly 15'))
        if sub != 15:
            raise ValidationError(
                _('Substitute electors must be exactly 15'))
    else:
        if regular != 11:
            raise ValidationError(
                _('Regular electors must be exactly 11'))
        if sub != 11:
            raise ValidationError(
                _('Substitute electors must be exactly 11'))
