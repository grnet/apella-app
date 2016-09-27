from rest_framework import serializers
from datetime import timedelta


def validate_dates_interval(start, end):
    if end - timedelta(days=30) < start:
        raise serializers.ValidationError(
            'End date should be 30 days after start date')


class PositionMixin(object):

    def create(self, validated_data):
        ends_at = validated_data['ends_at']
        starts_at = validated_data['starts_at']
        validate_dates_interval(starts_at, ends_at)

        return super(PositionMixin, self).create(validated_data)
