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
