import json
import os
from django.conf import settings


def load_resources():
    with open(os.path.join(settings.RESOURCES_DIR, 'common.json')) as json_file:
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
