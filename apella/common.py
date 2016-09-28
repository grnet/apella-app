import json
from django.conf import settings


def load_resources():
    with open(settings.RESOURCES_FILE) as json_file:
        return json.load(json_file)


RESOURCES = load_resources()
USER_ROLES = RESOURCES['USER_ROLES']
POSITION_STATES = RESOURCES['POSITION_STATES']
CANDIDACY_STATES = RESOURCES['CANDIDACY_STATES']
REGISTRY_TYPES = RESOURCES['REGISTRY_TYPES']
