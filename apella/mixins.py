from django.conf import settings
from django.apps import apps
from collections import defaultdict
from apella.models import ApellaUser
from apella.validators import validate_dates_interval, validate_position_dates
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


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


def create_lang_objects(model_name, lang_data):

    lang_objects = defaultdict(dict)
    for lang, data in lang_data.iteritems():
        if data:
            model_name_lang = model_name + lang.capitalize()
            model = apps.get_model(
                app_label='apella', model_name=model_name_lang)
            lang_objects[lang] = model.objects.create(**data)
    return lang_objects


def update_lang_object(model_name, instance, lang, lang_data):
    lang_object = None
    if lang_data:
        model_name_lang = model_name + lang.capitalize()
        model = apps.get_model(
            app_label='apella', model_name=model_name_lang)
        lang_object = getattr(instance, lang)
        if lang_object:
            for field in lang_data:
                setattr(lang_object, field, lang_data.get(field))
                lang_object.save()
        else:
            lang_object = model.objects.create(**lang_data)
    return lang_object


def lang_to_fields(data):
    v = defaultdict(dict)
    for field, value in data.items():
        pop = False
        for lang in settings.LANGUAGES:
            try:
                locale_value = value.get(lang)
                if locale_value:
                    v[lang][field] = locale_value
                    pop = True
            except AttributeError:
                pass
        if pop:
            data.pop(field)
    data.update(v)
    return data


def fields_to_lang(data):
    v = defaultdict(dict)
    for lang in settings.LANGUAGES:
        locale = data.pop(lang, None)
        if locale:
            for key, value in locale.iteritems():
                v[key][lang] = value
                data.update(v)
    return data


class NestedWritableObjectsMixin(object):

    def create(self, validated_data):
        """
        Overrides serializer's create method to create nested
        objects in advance.
        If nested object is a user object it should be created before
        its parent, along with its language nested objects.
        """
        model_name = self.Meta.model.__name__
        model = apps.get_model(app_label='apella', model_name=model_name)

        has_user = False
        if 'user' in validated_data:
            has_user = True
            user_data = validated_data.pop('user')
            user_locales = defaultdict(dict)
            for lang in settings.LANGUAGES:
                user_locales[lang] = user_data.pop(lang, None)

            user_lang_objects = create_lang_objects(
                'ApellaUser', user_locales)
            apella_user = ApellaUser.objects.create(
                el=user_lang_objects.get('el'),
                en=user_lang_objects.get('en'),
                **user_data)

        locales = defaultdict(dict)
        for lang in settings.LANGUAGES:
            locales[lang] = validated_data.pop(lang, None)

        if has_user:
            obj = model.objects.create(user=apella_user, **validated_data)
        else:
            obj = model.objects.create(**validated_data)

        lang_objects = create_lang_objects(model_name, locales)
        for lang, lang_object in lang_objects.iteritems():
            setattr(obj, lang, lang_object)
        obj.save()

        return obj

    def update(self, instance, validated_data):
        """
        Overrides serializer's update method to update nested objects
        in advance.
        """

        model_name = self.Meta.model.__name__
        for lang in settings.LANGUAGES:
            lang_object = update_lang_object(
                model_name, instance, lang, validated_data.pop(lang, None))
            setattr(instance, lang, lang_object)

        if 'user' in validated_data:
            user_data = validated_data.pop('user')
            apella_user = ApellaUser.objects.get(
                username=user_data.get('username'))
            for lang in settings.LANGUAGES:
                lang_object = update_lang_object(
                    'ApellaUser', apella_user, lang, user_data.pop(lang, None))
                setattr(apella_user, lang, lang_object)

            for k, v in user_data.iteritems():
                setattr(apella_user, k, v)

            apella_user.save()

        for key, value in validated_data.iteritems():
            setattr(instance, key, value)

        instance.save()
        return instance

    def to_internal_value(self, data):
        """
        Remove UniqueValidator from username if updating
        parent object
        """
        data = lang_to_fields(data)
        if self.context.get('request').method == 'PUT' and \
                'user.username' in data:
            try:
                obj_id = self.fields['user']['username'].\
                    to_internal_value(data['user.username'])
            except serializers.ValidationError as exc:
                raise serializers.ValidationError(
                    {'user': {'username': exc.detail}})
            field = self.fields['user']['username']
            for validator in field.validators:
                if type(validator) == UniqueValidator:
                    validator.queryset = validator.queryset.exclude(
                        username=obj_id)
        return super(NestedWritableObjectsMixin, self).to_internal_value(data)

    def to_representation(self, instance):
        data = super(NestedWritableObjectsMixin, self).to_representation(
            instance)
        data = fields_to_lang(data)
        try:
            user_data = data.pop('user')
            user_data = fields_to_lang(user_data)
            data['user'] = user_data
        except KeyError:
            pass
        return data
