from os.path import join
import json
import yaml
from cerberus import Validator
import os
from django.conf import settings

from apimas.exceptions import ApimasException
from collections import defaultdict
from apella.util import safe_path_join


VALIDATION_SCHEMA = {
    'root': {
        'type': 'string'
    },
    'spec': {
         'type': 'dict'
    }
}


def rule_to_dict(data, args):
    if len(args) == 1:
        return args[0]

    key = args.pop(0)
    for k in key.split(","):
        k = k.strip()
        data[k] = data[k] if k in data else {}
        partial = {
            k: rule_to_dict(data[k], args)
        }
        data.update(partial)
    return data


def load_permissions():
    PERMISSIONS = defaultdict(lambda: dict)
    for rule in settings.PERMISSION_RULES:
        rule_to_dict(PERMISSIONS, list(rule))
    return PERMISSIONS


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
    with open(safe_path_join(settings.RESOURCES_DIR, 'common.json')) \
            as json_file:
        return json.load(json_file)


def load_holidays():
    with open(safe_path_join(settings.RESOURCES_DIR, 'holidays.json')) \
            as json_file:
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
FILE_SOURCE = RESOURCES['FILE_SOURCE']
APPLICATION_TYPES = RESOURCES['APPLICATION_TYPES']
APPLICATION_STATES = RESOURCES['APPLICATION_STATES']
POSITION_TYPES = RESOURCES['POSITION_TYPES']
POSITION_RANKS = RESOURCES['POSITION_RANKS']

FILE_KIND_TO_FIELD = {
    "cv": {
        "field": "cv",
        "many": False,
    },
    "cv_professor": {
        "field": "cv_professor",
        "many": False,
    },
    "diploma": {
        "field": "diplomas",
        "many": True,
    },
    "publication": {
        "field": "publications",
        "many": True,
    },
    "id_passport": {
        "field": "id_passport_file",
        "many": False,
    },
    "electors_set_file": {
        "field": "electors_set_file",
        "many": False,
    },
    "committee_set_file": {
        "field": "committee_set_file",
        "many": False,
    },
    "committee_proposal": {
        "field": "committee_proposal",
        "many": False,
    },
    "committee_note": {
        "field": "committee_note",
        "many": False,
    },
    "electors_meeting_proposal": {
        "field": "electors_meeting_proposal",
        "many": False,
    },
    "nomination_proceedings": {
        "field": "nomination_proceedings",
        "many": False,
    },
    "proceedings_cover_letter": {
        "field": "proceedings_cover_letter",
        "many": False,
    },
    "nomination_act": {
        "field": "nomination_act",
        "many": False,
    },
    "revocation_decision": {
        "field": "revocation_decision",
        "many": False,
    },
    "failed_election_decision": {
        "field": "failed_election_decision",
        "many": False,
    },
    "assistant_files": {
        "field": "assistant_files",
        "many": True,
    },
    "self_evaluation_report": {
        "field": "self_evaluation_report",
        "many": False,
    },
    "attachment_files": {
        "field": "attachment_files",
        "many": True,
    },
    "registry_set_decision_file": {
        "field": "registry_set_decision_file",
        "many": False,
    },
}
