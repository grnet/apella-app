from collections import defaultdict

from django.conf import settings
from django.apps import apps
from django.http.request import QueryDict
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apella.models import ApellaUser, Position


class ValidatorMixin(object):

    def validate(self, data):
        model = self.Meta.model
        instance = model(**data)
        instance.clean()
        return super(ValidatorMixin, self).validate(data)


class PositionValidatorMixin(ValidatorMixin):

    def validate(self, data):
        committee = data.pop('committee', [])
        electors = data.pop('electors', [])
        assistants = data.pop('assistants', [])
        data = super(PositionValidatorMixin, self).validate(data)
        data['committee'] = committee
        data['electors'] = electors
        data['assistants'] = assistants

        return data


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


def fields_to_lang(data):
    """
    if data == {'title': {'el': 'title_el', 'en': 'title_en'}}
    return {'el': {'title': 'title_el'}, 'en': {'title': 'title_en'}}
    """
    v = defaultdict(dict)
    for key, value in data.iteritems():
        for lang in settings.LANGUAGES:
            if type(value) == dict:
                v[lang][key] = value.get(lang, None)
            else:
                v[key] = value
    return v


def lang_to_fields(data):
    """
    if data == {'el': {'title': 'title_el'}, 'en': {'title': 'title_en'}}
    return {'title': {'el': 'title_el', 'en': 'title_en'}}
    """
    v = defaultdict(dict)
    for key, value in data.iteritems():
        if key in settings.LANGUAGES and value:
            for field, field_value in value.iteritems():
                v[field][key] = field_value
        else:
            v[key] = value
    return v


class NestedWritableObjectsMixin(object):

    def create(self, validated_data):
        """
        Overrides serializer's create method to create nested
        objects in advance.
        """
        model_name = self.Meta.model.__name__
        model = self.Meta.model

        locales = defaultdict(dict)
        for lang in settings.LANGUAGES:
            locales[lang] = validated_data.pop(lang, None)
        lang_objects = create_lang_objects(model_name, locales)
        for lang, lang_object in lang_objects.iteritems():
            validated_data[lang] = lang_object

        if model_name == 'ApellaUser':
            obj = model.objects.create_user(**validated_data)
        else:
            obj = model.objects.create(**validated_data)

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

        for key, value in validated_data.iteritems():
            if model_name == 'ApellaUser' and key == 'password':
                instance.set_password(value)
            else:
                setattr(instance, key, value)

        instance.save()
        return instance

    def to_internal_value(self, data):
        data = fields_to_lang(data)

        return super(NestedWritableObjectsMixin, self).to_internal_value(data)

    def to_representation(self, instance):
        data = super(NestedWritableObjectsMixin, self).to_representation(
            instance)
        data = lang_to_fields(data)

        return data


class NestedWritableUserMixin(NestedWritableObjectsMixin):

    NESTED_USER_KEY = 'user'

    def __init__(self, *args, **kwargs):
        super(NestedWritableUserMixin, self).__init__(*args, **kwargs)
        if self.context.get('request').method == 'PUT' and\
                self.NESTED_USER_KEY in self.fields:
            self.fields['user'].fields['username'].read_only = True

    def create(self, validated_data):
        model_name = self.Meta.model.__name__
        model = apps.get_model(app_label='apella', model_name=model_name)

        user_data = validated_data.pop(self.NESTED_USER_KEY)
        user_locales = defaultdict(dict)
        for lang in settings.LANGUAGES:
            user_locales[lang] = user_data.pop(lang, None)

        user_lang_objects = create_lang_objects(
            'ApellaUser', user_locales)
        apella_user = ApellaUser.objects.create_user(
            el=user_lang_objects.get('el'),
            en=user_lang_objects.get('en'),
            **user_data)
        validated_data[self.NESTED_USER_KEY] = apella_user

        return super(NestedWritableUserMixin, self).create(validated_data)

    def update(self, instance, validated_data):

        model_name = self.Meta.model.__name__

        user_data = validated_data.pop(self.NESTED_USER_KEY)
        apella_user = instance.user
        for lang in settings.LANGUAGES:
            lang_object = update_lang_object(
                'ApellaUser', apella_user, lang, user_data.pop(lang, None))
            setattr(apella_user, lang, lang_object)

        for k, v in user_data.iteritems():
            if k == 'password':
                apella_user.set_password(v)
            else:
                setattr(apella_user, k, v)

        apella_user.save()

        return super(NestedWritableUserMixin, self).update(
            instance, validated_data)

    def to_internal_value(self, data):
        user_data = fields_to_lang(data.pop(self.NESTED_USER_KEY))
        data[self.NESTED_USER_KEY] = user_data

        return super(NestedWritableUserMixin, self).to_internal_value(data)

    def to_representation(self, instance):
        data = super(NestedWritableUserMixin, self).to_representation(
            instance)
        user_data = data.pop(self.NESTED_USER_KEY)
        user_data = lang_to_fields(user_data)
        data[self.NESTED_USER_KEY] = user_data

        return data
