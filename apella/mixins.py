from rest_framework import serializers
from datetime import timedelta
from apella_app import settings


def validate_dates_interval(start, end, interval):
    if end - start < timedelta(days=interval):
        raise serializers.ValidationError(
            'End date should be %s days after start date' % interval)


class PositionMixin(object):

    def validate(self, data):
        validate_dates_interval(
            data['starts_at'],
            data['ends_at'],
            settings.START_DATE_END_DATE_INTERVAL)
        return super(PositionMixin, self).validate(data)
