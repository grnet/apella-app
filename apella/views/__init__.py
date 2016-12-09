import json

from apella.permissions.permission_rules import PERMISSION_RULES
from apella.common import load_resources, load_permissions, load_holidays

from django.http import HttpResponse

def config(request):
    resources = load_resources()
    permissions = load_permissions()
    holidays = load_holidays()

    config_data = {
        'resources': resources,
        'permissions': permissions,
        'holidays': holidays
    }
    return HttpResponse(json.dumps(config_data), content_type='application/json')
