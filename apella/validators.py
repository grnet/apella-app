from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.utils import timezone


def before_today_validator(value):
    now = timezone.now().date() if type(value) is date else timezone.now()
    if value and value > now:
        raise ValidationError(_('Date should be before today'))


def after_today_validator(value):
    now = timezone.now().date() if type(value) is date else timezone.now()
    if value and value < now:
        raise ValidationError(_('Date should be after today'))


def validate_dates_interval(start, end, interval):
    if end - start < timedelta(days=interval):
        raise ValidationError(
            _('End date should be %s days after start date' % interval))


def validate_position_dates(start, end):
    if timezone.now() < start:
        raise ValidationError(_('Position opens at %s' % start))
    if timezone.now() > end:
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
