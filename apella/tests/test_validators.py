from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.test import TestCase
from apella.validators import before_today_validator, after_today_validator,\
        validate_dates_interval
from django.conf import settings


class ValidatorTest(TestCase):

    def test_before_today_validaror(self):
        date = datetime.now() + timedelta(days=1)
        self.assertRaises(ValidationError, before_today_validator, date)
        self.assertRaises(ValidationError, before_today_validator, date.date())

        date -= timedelta(days=1)
        before_today_validator(date)
        before_today_validator(None)

    def test_after_today_validaror(self):
        date = datetime.now() - timedelta(days=1)
        self.assertRaises(ValidationError, after_today_validator, date)
        self.assertRaises(ValidationError, after_today_validator, date.date())

        date += timedelta(days=2)
        after_today_validator(date)
        after_today_validator(None)

    def test_validate_dates_interval(self):
        start = datetime.now()
        end = start + timedelta(days=29)
        self.assertRaises(
            serializers.ValidationError,
            validate_dates_interval,
            start,
            end,
            settings.START_DATE_END_DATE_INTERVAL)

        end += timedelta(days=1)
        validate_dates_interval(
            start, end, settings.START_DATE_END_DATE_INTERVAL)
