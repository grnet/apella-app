import json
import urlparse
import logging
logger = logging.getLogger(__name__)

from apella.common import load_resources, load_permissions, load_holidays
from apella.models import Professor, OldApellaAreaSubscriptions

from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt


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


def get_evaluators_auth_token():
    try:
        with open(settings.EVALUATORS_AUTH_TOKEN_FILE) as f:
            token = f.read().strip()
        m = "read evaluators auth token from %r"
        m %= settings.EVALUATORS_AUTH_TOKEN_FILE
        logger.info(m)
        return token
    except Exception as e:
        logger.exception(e)
        if not settings.DEBUG:
            raise
    return None

def get_evaluators_allow_addr():
    try:
        with open(settings.EVALUATORS_ALLOW_ADDR_FILE) as f:
            allow_addr = json.load(f)
        m = "read evaluators allow address list from %r"
        m %= settings.EVALUATORS_ALLOW_ADDR_FILE
        logger.info(m)
        return allow_addr
    except Exception as e:
        logger.exception(e)
        if not settings.DEBUG:
            raise
    return None

EVALUATORS_AUTH_TOKEN = get_evaluators_auth_token()
EVALUATORS_ALLOW_ADDR = get_evaluators_allow_addr()


@csrf_exempt
def evaluators(request, email):
    if request.method.upper() != 'POST':
        m = "evaluators unauthorized method: %r"
        m %= request.method
        return HttpResponse('only POST method is allowed\n', status=405)

    if request.META.get('HTTP_X_AUTH_TOKEN') != EVALUATORS_AUTH_TOKEN:
        m = "evaluators unauthorized x-auth-token: %r"
        m %= request.META.get('HTTP_X_AUTH_TOKEN')
        logger.warn(m)
        return HttpResponse('no x-auth-token header\n', status=403)

    remote_addr = request.META.get('HTTP_X_FORWARDED_FOR')
    remote_addr = remote_addr.split(',')[0].strip()
    m = "REMOTE_ADDR %r" % remote_addr
    logger.info(m)
    if remote_addr not in EVALUATORS_ALLOW_ADDR:
        m = "evaluators unauthorized address: %r"
        m %= remote_addr
        logger.warn(m)
        return HttpResponse('not from your IP address\n', status=403)

    try:
	p = Professor.objects.get(user__email=email, is_foreign=False,
                                  is_verified=True, user__is_active=True)
    except Professor.DoesNotExist:
        return HttpResponse('professor does not exist\n', status=404)

    institution = p.institution.title.el if p.institution \
        else p.institution_freetext
    department = p.department.title.el if p.department \
        else ''

    if not p.user.old_user_id:
        interests = []
    else:
        subscriptions = OldApellaAreaSubscriptions.objects
        subscriptions = subscriptions.filter(
            user_id=p.user.old_user_id, locale='el')
        interests_set = set(subscriptions.values_list('subject_name', flat=True))
        interests = list(interests_set)

    professor_data = {
        'person': {
            'id': p.user.id,
            'email': p.user.email,
            'surname': p.user.last_name.el,
            'name': p.user.first_name.el,
            'fathername': p.user.father_name.el,
            'rank': p.rank,
            'institution': institution,
            'department': department,
            'government_gazette_no': p.fek,
            'discipline_text': p.discipline_text,
            'interests': interests,
        }
    }
    body = json.dumps(professor_data, ensure_ascii=False, indent=2) + '\n'
    return HttpResponse(body, content_type='application/json')
