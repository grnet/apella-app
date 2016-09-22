from datetime import datetime, date, timedelta
from django.core.exceptions import ValidationError


def before_today_validator(value):
    """
    Checks if the given object (date or datetime) preceeds today

    :param value: Date or Datetime object

    :raises ValidationError if given date succeeds today
    """
    now = datetime.now().date() if type(value) is date else datetime.now()
    if value and value > now:
        raise ValidationError('Date should be before today')


def after_today_validator(value):
    """
    Checks if the given object (date or datetime) succeeds today

    :param value: Date or Datetime object

    :raises ValidationError if given date preceeds today
    """
    now = datetime.now().date() if type(value) is date else datetime.now()
    if value and value < now:
        raise ValidationError('Date should be after today')
