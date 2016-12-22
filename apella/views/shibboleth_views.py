import base64
import json
import urlparse
import logging
import urllib
import uuid

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import transaction

from apella.models import ApellaUser, Professor, MultiLangFields, \
    RegistrationToken
from apella import auth_hooks


logger = logging.getLogger('shibboleth')

ABNORMAL_HEADERS = [
    'HTTP_EPPN', 'HTTP_REMOTE_USER'
]


def shibboleth_headers(headers):
    for key, val in headers.iteritems():
        if key in ABNORMAL_HEADERS or key.startswith('HTTP_SHIB'):
            key = key.lstrip('HTTP_')
            key = key.lstrip('SHIB_')
            yield key.lower(), val


SHIBBOLETH_USER_MAP = {
    'name': 'first_name',
    'mail': 'email'
}
MULTILANG_FIELDS = ['first_name', 'last_name', 'father_name'];

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
def login(request):
    force_register = request.GET.get('register', False)
    force_login = request.GET.get('login', False) or (not force_register)

    token_login_url = settings.TOKEN_LOGIN_URL
    token_register_url = settings.TOKEN_REGISTER_URL

    headers = request.META
    debug_headers = getattr(settings, 'DEBUG_SHIBBOLETH_HEADERS', {})
    if settings.DEBUG and headers:
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
            msg = 'user.not.verified'
            return HttpResponseRedirect(token_login_url + "#error=%s" % msg)

        if not user.is_verified:
            msg = 'user.not.moderated'
            return HttpResponseRedirect(token_login_url + "#error=%s" % msg)

        token = auth_hooks.login_user(user.user, request)
        token = token.key

    except UserModel.DoesNotExist:
        if force_login:
            msg = "user.not.found"
            return HttpResponseRedirect(token_login_url + "#error=%s" % msg)
        token = create_registration_token(identifier, user_data)
        created = True

    if created:
        data = urllib.quote(base64.b64encode(json.dumps(user_data)))
        redirect_url = token_register_url
        token_fragment = '?initial=%s#token=%s' % (data, token)
    else:
        redirect_url = token_login_url
        token_fragment = '#token=' + token

    redirect_url = redirect_url + token_fragment
    return HttpResponseRedirect(redirect_url)
