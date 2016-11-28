from collections import defaultdict

from django.conf import settings
from django.apps import apps
from django.http.request import QueryDict
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.utils import model_meta

from apella.models import ApellaUser, Position, MultiLangFields


class ValidatorMixin(object):

    def validate(self, data):
        model = self.Meta.model
        instance = model(**data)
        instance.clean()
        return super(ValidatorMixin, self).validate(data)


def get_dep_number(data):
    dep_number = data['department'].dep_number
    if not dep_number:
        raise serializers.ValidationError(
            {"dep_number":
                "You should first set DEP number for Department: %s"
                % data['department'].title.en})
    return dep_number


class Position(ValidatorMixin):

    def validate(self, data):
        committee = data.pop('committee', [])
        electors = data.pop('electors', [])
        assistants = data.pop('assistants', [])
        data = super(Position, self).validate(data)
        data['committee'] = committee
        data['electors'] = electors
        data['assistants'] = assistants

        return data

    def create(self, validated_data):
        validated_data['department_dep_number'] = \
            get_dep_number(validated_data)
        return super(Position, self).create(validated_data)


def create_objects(model, fields, validated_data):
    """
    Recursively creates nested objects.
    """
    for field_name, field in fields.iteritems():
        if isinstance(field, serializers.BaseSerializer) \
                and field_name in validated_data:
            nested_data = validated_data.pop(field_name, None)
            nested_object = create_objects(
                field.Meta.model, field.get_fields(), nested_data)
            validated_data[field_name] = nested_object

    info = model_meta.get_field_info(model)
    many_to_many = {}
    for field_name, relation_info in info.relations.items():
        if relation_info.to_many and (field_name in validated_data):
            many_to_many[field_name] = validated_data.pop(field_name)

    if isinstance(model, ApellaUser):
        obj = model.objects.create_user(**validated_data)
    else:
        obj = model.objects.create(**validated_data)

    if many_to_many:
        for field_name, value in many_to_many.items():
            setattr(obj, field_name, value)
    return obj


def update_objects(fields, validated_data, instance=None, model=None):
    """
    Recursively updated nested objects.
    """
    if not instance:
        return create_objects(model, fields, validated_data)
    info = model_meta.get_field_info(type(instance))
    many_to_many = {}
    for field_name, relation_info in info.relations.items():
        if relation_info.to_many and (field_name in validated_data):
            many_to_many[field_name] = validated_data.pop(field_name)

    for field_name, field in fields.iteritems():
        if isinstance(field, serializers.BaseSerializer) \
                and field_name in validated_data:
            nested_data = validated_data.pop(field_name, None)
            nested_object = update_objects(
                field.get_fields(), nested_data,
                instance=getattr(instance, field_name), model=field.Meta.model)
            setattr(instance, field_name, nested_object)
        elif field_name in validated_data:
            if field_name == 'password':
                instance.set_password(validated_data.get(field_name))
            else:
                setattr(instance, field_name, validated_data.get(field_name))
    if many_to_many:
        for field_name_many, value in many_to_many.items():
            setattr(instance, field_name_many, value)
    instance.save()
    return instance


class NestedWritableObjectsMixin(object):

    NESTED_USER_KEY = 'user'

    def __init__(self, *args, **kwargs):
        super(NestedWritableObjectsMixin, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and \
                (request.method == 'PUT' or request.method == 'PATCH') and \
                self.NESTED_USER_KEY in self.fields:
            self.fields[self.NESTED_USER_KEY].fields['username'].read_only = \
                    True

    def create(self, validated_data):
        model = self.Meta.model
        obj = create_objects(model, self.get_fields(), validated_data)
        return obj

    def update(self, instance, validated_data):
        instance = update_objects(
            self.get_fields(), validated_data, instance=instance)
        return instance
