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
