from os.path import join
import json
import yaml
from cerberus import Validator
import os
from django.conf import settings

from apimas.modeling.core.exceptions import ApimasException

VALIDATION_SCHEMA = {
    'root': {
        'type': 'string'
    },
    'spec': {
         'type': 'dict'
    }
}


def load_config():
    config = join(settings.RESOURCES_DIR, settings.CONFIG_FILE)
    with open(config) as data_file:
        data = yaml.load(data_file)
        validator = Validator(VALIDATION_SCHEMA)
        is_valid = validator.validate(data)
        if not is_valid:
            raise ApimasException(validator.errors)
    return data


def load_resources():
    with open(os.path.join(settings.RESOURCES_DIR, 'www/common.json')) as json_file:
        return json.load(json_file)


RESOURCES = load_resources()
USER_ROLES = RESOURCES['USER_ROLES']
POSITION_STATES = RESOURCES['POSITION_STATES']
CANDIDACY_STATES = RESOURCES['CANDIDACY_STATES']
REGISTRY_TYPES = RESOURCES['REGISTRY_TYPES']
AUTHORITIES = RESOURCES['AUTHORITIES']
MANAGER_ROLES = RESOURCES['MANAGER_ROLES']
RANKS = RESOURCES['RANKS']
FILE_KINDS = RESOURCES['FILE_KINDS']
INSTITUTION_CATEGORIES = RESOURCES['INSTITUTION_CATEGORIES']
