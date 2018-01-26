from datetime import datetime, timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase

from apella.validators import before_today_validator, after_today_validator,\
        validate_dates_interval


class ValidatorTest(TestCase):

    def test_before_today_validaror(self):
        date = datetime.now() + timedelta(days=1)
        self.assertRaises(ValidationError, before_today_validator, date)

        date -= timedelta(days=2)
        before_today_validator(date)

    def test_after_today_validaror(self):
        date = datetime.now() - timedelta(days=1)
        self.assertRaises(ValidationError, after_today_validator, date)

        date += timedelta(days=2)
        after_today_validator(date)

    def test_validate_dates_interval(self):
        start = datetime.now()
        end = start + timedelta(days=28)
        self.assertRaises(
            ValidationError,
            validate_dates_interval,
            start,
            end,
            settings.START_DATE_END_DATE_INTERVAL)

        end += timedelta(days=1)
        validate_dates_interval(
            start, end, settings.START_DATE_END_DATE_INTERVAL)
