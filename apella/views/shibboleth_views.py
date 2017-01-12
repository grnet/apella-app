import base64
import json
import urlparse
import logging
import urllib
import uuid
import re

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import transaction

from apella.models import ApellaUser, Professor, MultiLangFields, \
    RegistrationToken
from apella import auth_hooks


LEGACY_URL = getattr(settings, 'APELLA_LEGACY_ACADEMIC_LOGIN_URL')
MIGRATE_LEGACY = bool(LEGACY_URL)

logger = logging.getLogger(__name__)

ABNORMAL_HEADERS = [
    'HTTP_EPPN', 'HTTP_REMOTE_USER'
]


def shibboleth_headers(headers):
    for key, val in headers.iteritems():
        if key in ABNORMAL_HEADERS or key.startswith('HTTP_SHIB'):
            key = re.sub('^HTTP_', '', key)
            key = re.sub('^SHIB_', '', key)
            yield key.lower(), val


SHIBBOLETH_USER_MAP = {
    'name': 'first_name',
    'mail': 'email'
}
MULTILANG_FIELDS = ['first_name', 'last_name', 'father_name'];


def make_migration_key(identifier):
    return str(uuid.uuid4())


def get_user_data(shib_data):
    """
    Extract user model fields from shibboleth data.
    """
    result = {}
    lang = settings.LANGUAGE_CODE.split('-')[0]
    for key, val in shib_data.iteritems():
        if key in SHIBBOLETH_USER_MAP:
            userKey = SHIBBOLETH_USER_MAP[key]
            if userKey in MULTILANG_FIELDS:
                val = {lang: val}
            result[userKey] = val
    return result



def is_eligible_shibboleth_user(data):
    # hook to validate that all required fields are set or to apply other
    # validation rules
    # raise ValidationError
    return data


def model_from_data(data):
    return Professor


def create_registration_token(identifier, data):
    data = json.dumps(data)
    token = RegistrationToken.objects.create(
        token=str(uuid.uuid4()), identifier=identifier, data=data)
    return token.token


@transaction.atomic
def legacy_login(request):
    headers = request.META
    debug_headers = getattr(settings, 'DEBUG_SHIBBOLETH_HEADERS_LEGACY', {})
    if settings.DEBUG and debug_headers:
        headers = debug_headers

    shibboleth_data = dict(zip(*zip(*shibboleth_headers(headers))))
    identifier = shibboleth_data.get('remote_user', None)

    key = request.GET.get('migration_key', None)
    legacy_id = identifier
    if not key or not legacy_id:
        url = urlparse.urljoin(
            settings.API_HOST, settings.TOKEN_LOGIN_URL)
        return HttpResponseRedirect(url + "#error=legacy.error")

    id = auth_hooks.init_legacy_migration(legacy_id, key)
    if id is None:
        url = urlparse.urljoin(
            settings.API_HOST, reverse('shibboleth_login'))
        return HttpResponseRedirect(url + "?login=1&migrate=0")

    params = "?login=1&migrate=%s"
    url = urlparse.urljoin(settings.API_HOST, reverse('shibboleth_login'))
    return HttpResponseRedirect(url + params % str(id))



@transaction.atomic
def login(request):
    force_register = request.GET.get('register', False)
    force_login = request.GET.get('login', False) or (not force_register)

    migrate_id = request.GET.get('migrate', None)

    token_login_url = settings.TOKEN_LOGIN_URL
    token_register_url = settings.TOKEN_REGISTER_URL

    headers = request.META
    debug_headers = getattr(settings, 'DEBUG_SHIBBOLETH_HEADERS', {})
    if settings.DEBUG and debug_headers:
        headers = debug_headers

    shibboleth_data = dict(zip(*zip(*shibboleth_headers(headers))))
    identifier = shibboleth_data.get('remote_user', None)

    if not identifier:
        return HttpResponseBadRequest("invalid identifier")

    try:
        is_eligible_shibboleth_user(shibboleth_data)
    except ValidationError, e:
        logger.info('data not accepted %r: %r', shibboleth_data, e.message)
        return HttpResponseBadRequest(e.message)

    # resolve which user model class should be used to lookup/create user
    UserModel = model_from_data(shibboleth_data)
    user_data = get_user_data(shibboleth_data)
    logger.debug('login %r', user_data)

    user = None
    token = None
    created = False

    if migrate_id and migrate_id != "0":
        s_identifier = request.session.pop('shibboleth_id', None)
        migration_key = request.session.pop('migration_key', None)
        if s_identifier != identifier:
            logger.error("forged migration")
            raise PermissionDenied("forged migration handshake")

        legacy = auth_hooks.migrate_legacy(
            migration_key, migrate_id, identifier)
        logger.info("legacy id %s migrated to %s", legacy, identifier)

    request.session.pop('shibboleth_id', None)
    request.session.pop('migration_key', None)

    try:
        user = UserModel.objects.get(user__shibboleth_id=identifier)

        if force_register:
            msg = "user.exists"
            return HttpResponseRedirect(token_login_url + "#error=%s" % msg)

        # user not active
        if not user.user.is_active:
            msg = 'user.not.active'
            return HttpResponseRedirect(token_login_url + "#error=%s" % msg)

        if not user.user.email_verified:
            msg = 'user.not.email_verified'
            return HttpResponseRedirect(token_login_url + "#error=%s" % msg)

        token = auth_hooks.login_user(user.user, request)
        token = token.key

    except UserModel.DoesNotExist:

        if force_login and MIGRATE_LEGACY and not migrate_id:
            migration_key = make_migration_key(identifier)
            request.session['shibboleth_id'] = identifier
            request.session['migration_key'] = migration_key
            url = LEGACY_URL + "?migrate=1&migration_key=%s" % migration_key
            logger.info("redirect to legacy shibboleth login url")
            return HttpResponseRedirect(url)

        if force_login:
            msg = "user.not.found"
            return HttpResponseRedirect(token_login_url + "#error=%s" % msg)

        token = create_registration_token(identifier, user_data)
        created = True

    if created:
        data = urllib.quote(base64.b64encode(json.dumps(user_data)))
        redirect_url = token_register_url
        token_fragment = '?initial=%s&academic=1&#token=%s' % (data, token)
    else:
        redirect_url = token_login_url
        token_fragment = '#token=' + token

    redirect_url = redirect_url + token_fragment
    return HttpResponseRedirect(redirect_url)
