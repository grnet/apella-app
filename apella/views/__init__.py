import json
import urlparse

from apella.permissions.permission_rules import PERMISSION_RULES
from apella.common import load_resources, load_permissions, load_holidays
from django.conf import settings

from django.http import HttpResponse

def config(request):
    host = getattr(settings, 'API_HOST', None)
    prefix = getattr(settings, 'API_PREFIX', '')
    api_endpoint = urlparse.urljoin(prefix, 'api')

    if host is None:
        host = request.build_absolute_uri('/')

    backend_host = urlparse.urljoin(host, api_endpoint)

    resources = load_resources()
    permissions = load_permissions()
    holidays = load_holidays()

    config_data = {
        'resources': resources,
        'permissions': permissions,
        'holidays': holidays,
        'host': host,
        'prefix': prefix,
        'api_endpoint': api_endpoint,
        'backend_host': backend_host
    }
    return HttpResponse(json.dumps(config_data), content_type='application/json')
