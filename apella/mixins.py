from rest_framework import serializers
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from apella.models import InstitutionEl, InstitutionEn, Institution
from django.apps import apps
from collections import OrderedDict, defaultdict


def validate_dates_interval(start, end, interval):
    if end - start < timedelta(days=interval):
        raise serializers.ValidationError(
            'End date should be %s days after start date' % interval)


def validate_position_dates(start, end):
    if timezone.now() < start:
        raise serializers.ValidationError('Position opens at %s' % start)
    if timezone.now() > end:
        raise serializers.ValidationError('Position closed at %s' % end)


class PositionMixin(object):

    def validate(self, data):
        validate_dates_interval(
            data['starts_at'],
            data['ends_at'],
            settings.START_DATE_END_DATE_INTERVAL)
        return super(PositionMixin, self).validate(data)


class CandidacyMixin(object):

    def validate(self, data):
        validate_position_dates(
            data['position'].starts_at, data['position'].ends_at)
        return super(CandidacyMixin, self).validate(data)


class MultiLangMixin(object):

    def create(self, validated_data):

        model_name = self.Meta.model.__name__
        for lang in settings.LANGUAGES:
            locale = validated_data.get(lang, {})
            model_name_lang = model_name + lang.capitalize()
            model = apps.get_model(
                app_label='apella', model_name=model_name_lang)
            if locale:
                model_locale = model.objects.create(**locale)
                validated_data[lang] = model_locale

        return super(MultiLangMixin, self).create(validated_data)

    def update(self, instance, validated_data):

        model_name = self.Meta.model.__name__
        for lang in settings.LANGUAGES:
            locale = validated_data.pop(lang, None)
            model_name_lang = model_name + lang.capitalize()
            model = apps.get_model(
                app_label='apella', model_name=model_name_lang)
            if locale:
                model_locale = getattr(instance, lang)
                if model_locale:
                    for field in locale.keys():
                        setattr(model_locale, field, locale.get(field))
                        model_locale.save()
                else:
                    model_locale = model.objects.create(**locale)

                setattr(instance, lang, model_locale)
                instance.save()

        return super(MultiLangMixin, self).update(instance, validated_data)

    def to_representation(self, instance):
        data = super(MultiLangMixin, self).to_representation(instance)
        v = defaultdict(dict)
        for lang in settings.LANGUAGES:
            locale = data.pop(lang, None)
            if locale:
                for key, value in locale.iteritems():
                    v[key][lang] = value
                    data.update(v)
        return data
