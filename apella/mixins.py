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

    def __init__(self, *args, **kwargs):
        super(NestedWritableObjectsMixin, self).__init__(*args, **kwargs)
        if self.context.get('request').method == 'PUT' and\
                'user' in self.fields:
            self.fields['user'].fields['username'].read_only = True

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

        lang_objects = create_lang_objects(model_name, locales)
        for lang, lang_object in lang_objects.iteritems():
            validated_data[lang] = lang_object

        if has_user:
            obj = model.objects.create(user=apella_user, **validated_data)
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

        if 'user' in validated_data:
            user_data = validated_data.pop('user')
            apella_user = instance.user
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
        data = fields_to_lang(data)
        if 'user' in data:
            user_data = fields_to_lang(data.pop('user'))
            data['user'] = user_data
        return super(NestedWritableObjectsMixin, self).to_internal_value(data)

    def to_representation(self, instance):
        data = super(NestedWritableObjectsMixin, self).to_representation(
            instance)
        data = lang_to_fields(data)
        if 'user' in data:
            user_data = data.pop('user')
            user_data = lang_to_fields(user_data)
            data['user'] = user_data
        return data
