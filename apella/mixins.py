from rest_framework import serializers
from datetime import timedelta


def validate_dates_interval(start, end):
    if end - timedelta(days=30) < start:
        raise serializers.ValidationError(
            'End date should be 30 days after start date')


class PositionMixin(object):

    def validate(self, data):
        validate_dates_interval(data['starts_at'], data['ends_at'])
        return super(PositionMixin, self).validate(data)
