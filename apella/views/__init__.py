import json
import urlparse

from apella.permissions.permission_rules import PERMISSION_RULES
from apella.common import load_resources, load_permissions, load_holidays
from django.conf import settings
from django.core.urlresolvers import reverse


from django.http import HttpResponse

def config(request):
    base = getattr(settings, 'BASE_URL', None)
    prefix = getattr(settings, 'API_PREFIX', '')
    api_endpoint = urlparse.urljoin(prefix, 'api')
    shibboleth_endpoint = reverse('shibboleth_login')

    if base is None:
        base = request.build_absolute_uri('/')

    backend_host = urlparse.urljoin(base, api_endpoint)
    shibboleth_login_url = urlparse.urljoin(base, shibboleth_endpoint)

    resources = load_resources()
    permissions = load_permissions()
    holidays = load_holidays()

    config_data = {
        'resources': resources,
        'permissions': permissions,
        'holidays': holidays,
        'host': base,
        'prefix': prefix,
        'api_endpoint': api_endpoint,
        'backend_host': backend_host,
        'shibboleth_login_url': shibboleth_login_url
    }
    return HttpResponse(json.dumps(config_data),
                        content_type='application/json')
