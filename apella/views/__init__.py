import json
import urlparse

from apella.common import load_resources, load_permissions, load_holidays
from apella.models import Professor

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
    idp_whitelist = getattr(settings, 'SHIBBOLETH_IDP_WHITELIST', [])

    config_data = {
        'resources': resources,
        'permissions': permissions,
        'holidays': holidays,
        'host': base,
        'prefix': prefix,
        'api_endpoint': api_endpoint,
        'backend_host': backend_host,
        'shibboleth_login_url': shibboleth_login_url,
        'idp_whitelist': idp_whitelist
    }
    return HttpResponse(json.dumps(config_data),
                        content_type='application/json')


def evaluators(request, email):
    try:
        p = Professor.objects.get(user__email=email)
    except Professor.DoesNotExist:
        return HttpResponse(status=404)

    institution = p.institution.title.el if p.institution \
        else p.institution_freetext
    department = p.department.title.el if p.department \
        else ''

    professor_data = {
        'email': p.user.email,
        'surname': p.user.last_name.el,
        'name': p.user.first_name.el,
        'fathername': p.user.father_name.el,
        'rank': p.rank,
        'institution': institution,
        'department': department,
        'government_gazette_no': p.fek
    }
    return HttpResponse(json.dumps(professor_data),
                        content_type='application/json')
