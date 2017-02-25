import base64
import json
import urlparse
import logging
import urllib
import uuid
import re

from os import path
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import transaction

from apella.models import ApellaUser, Professor, MultiLangFields, \
    RegistrationToken, Institution
from apella.models import OldApellaUserMigrationData as OldUser
from apella import auth_hooks
from apella.util import urljoin


BASE_URL = settings.BASE_URL or '/';
API_PREFIX = settings.API_PREFIX

LEGACY_URL = getattr(settings, 'APELLA_LEGACY_ACADEMIC_LOGIN_URL', None)
LEGACY_PATH = ''
if LEGACY_URL:
    LEGACY_PATH = urlparse.urlparse(LEGACY_URL).path
MIGRATE_LEGACY = bool(LEGACY_URL)
TOKEN_LOGIN_URL = urljoin(BASE_URL, API_PREFIX, settings.TOKEN_LOGIN_URL)
TOKEN_REGISTER_URL = urljoin(BASE_URL, API_PREFIX, settings.TOKEN_REGISTER_URL)
LOG_SHIBBOLETH_DATA = getattr(settings, 'LOG_SHIBBOLETH_DATA', False)


logger = logging.getLogger(__name__)

ABNORMAL_HEADERS = [
    'HTTP_EPPN', 'HTTP_REMOTE_USER',
    'HTTP_AFFILIATION', 'HTTP_CN',
    'HTTP_DISPLAYNAME', 'HTTP_ENTITLEMENT',
    'HTTP_EPTID', 'HTTP_GIVENNAME',
    'HTTP_GREDUPERSON_UNDERGRADUATE_BRANCH',
    'HTTP_MAIL', 'HTTP_MOBILE_NUMBER',
    'HTTP_ORGUNIT_DN', 'HTTP_PERSISTENT_NAMEID',
    'HTTP_PRIMARY_AFFILIATION', 'HTTP_PRIMARY_ORGUNIT_DN',
    'HTTP_SCHAC_HOME_ORGANIZATION', 'HTTP_SCHAC_PERSONAL_UNIQUE_CODE',
    'HTTP_SN', 'HTTP_TELEPHONE_NUMBER', 'HTTP_TRANSIENT_ID',
    'HTTP_UNSCOPED_AFFILIATION'
]

EXCLUDED_HEADERS = [
    'HTTP_SHIB_SESSION_INDEX', 'HTTP_SHIB_SESSION_ID'
]

def shibboleth_headers(headers):
    for key, val in headers.iteritems():
        if key in EXCLUDED_HEADERS:
            continue
        if key in ABNORMAL_HEADERS or key.startswith('HTTP_SHIB'):
            key = re.sub('^HTTP_', '', key)
            key = re.sub('^SHIB_', '', key)
            yield key.lower(), val


SHIBBOLETH_USER_MAP = {
    'name': 'first_name',
    'mail': 'email',
    'displayname': 'first_name',
    'mobile_number': 'mobile_phone_number',
    'telephone_number': 'home_phone_number'
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


SHIBBOLETH_DISPLAY_DATA = getattr(settings, 'SHIBBOLETH_DISPLAY_DATA', [
    'name', 'displayname', 'cn', 'affiliation', 'orgunit_dn', 'givenname'
]);
def get_display_data(shib_data):
    """
    Filter shibboleth data for user display uses.
    """
    result = {}
    for key, val in shib_data.iteritems():
        if key in SHIBBOLETH_DISPLAY_DATA:
            result[key] = val
    return result


SHIBBOLETH_IDP_WHITELIST = getattr(settings, 'SHIBBOLETH_IDP_WHITELIST', [])
def is_eligible_shibboleth_user(data, legacy=False):
    scoped_affiliation = data.get('affiliation', None)
    primary_affiliation = data.get('primary_affiliation', None)
    unscoped_affiliation = data.get('unscoped_affiliation', None)
    affiliation = scoped_affiliation \
            or primary_affiliation \
            or unscoped_affiliation

    if not affiliation:
        raise ValidationError('no.affiliation')

    faculty = affiliation and 'faculty' in affiliation.lower()
    data['affiliation'] = affiliation

    if not faculty:
        m = ("no faculty in "
             "affiliation: %r, "
             "primary_affiliation: %r, "
             "unscoped_affiliation: %r")
        m %= (scoped_affiliation, primary_affiliation, unscoped_affiliation)
        logger.info(m)
        raise ValidationError('no.faculty')

    idp = data.get('identity_provider', None)
    if not idp:
        logger.info("non accepted idp %r", idp)
        raise ValidationError('no.idp')

    institutions = Institution.objects.filter(idp=idp)
    if not institutions.exists() and idp not in SHIBBOLETH_IDP_WHITELIST:
        logger.info("non accepted idp %r", idp)
        raise ValidationError('non.accepted.idp')

    return data


def model_from_data(data):
    return Professor


def create_registration_token(identifier, data, remote_data):
    data = json.dumps(data)
    remote_data = json.dumps(remote_data)
    token = RegistrationToken.objects.create(
        token=str(uuid.uuid4()), identifier=identifier, data=data,
        remote_data=remote_data)
    return token.token


@transaction.atomic
def legacy_login(request):
    headers = request.META
    debug_headers = getattr(settings, 'DEBUG_SHIBBOLETH_HEADERS_LEGACY', {})
    if settings.DEBUG and debug_headers:
        headers = debug_headers

    shibboleth_data = dict(zip(*zip(*shibboleth_headers(headers))))
    if LOG_SHIBBOLETH_DATA:
        m = "shibboleth data for %r: %r %r"
        m %= (request.path, shibboleth_data, headers.keys())
        logger.info(m)

    old_apella_shibboleth_id = shibboleth_data.get('remote_user', None)

    try:
        is_eligible_shibboleth_user(shibboleth_data, legacy=True)
    except ValidationError, e:
        logger.info('data not accepted %r: %r', shibboleth_data, e.message)
        return HttpResponseRedirect(TOKEN_LOGIN_URL+ "#error=%s" % e.message)

    key = request.GET.get('migration_key', None)
    if not key or not old_apella_shibboleth_id:
        url = TOKEN_LOGIN_URL
        return HttpResponseRedirect(url + "#error=legacy.error")

    old_user_exists = \
        auth_hooks.init_legacy_migration(old_apella_shibboleth_id, key)
    if not old_user_exists:
        url = urljoin(BASE_URL, reverse('shibboleth_login'))
        return HttpResponseRedirect(url + "?login=1&migrate=0")

    params = urllib.urlencode(
        {'login': 1, 'migrate': str(old_apella_shibboleth_id)})
    url = urljoin(BASE_URL, reverse('shibboleth_login'))
    return HttpResponseRedirect(url + '?' + params)



@transaction.atomic
def login(request):
    force_register = request.GET.get('register', False)
    force_login = request.GET.get('login', False) or (not force_register)
    enable_login = request.GET.get('enable-user', False)

    old_apella_shibboleth_id = request.GET.get('migrate', None)

    headers = request.META
    debug_headers = getattr(settings, 'DEBUG_SHIBBOLETH_HEADERS', {})
    if settings.DEBUG and debug_headers:
        headers = debug_headers

    shibboleth_data = dict(zip(*zip(*shibboleth_headers(headers))))
    if LOG_SHIBBOLETH_DATA:
        m = "shibboleth data for %r: %r %r"
        m %= (request.path, shibboleth_data, headers.keys())
        logger.info(m)

    apella2_shibboleth_id = shibboleth_data.get('remote_user', None)

    if not apella2_shibboleth_id:
        logger.info("cannot find remote_user in headers: %r" % shibboleth_data)
        return HttpResponseBadRequest("invalid identifier")

    try:
        is_eligible_shibboleth_user(shibboleth_data)
    except ValidationError, e:
        logger.info('data not accepted %r: %r', shibboleth_data, e.message)
        return HttpResponseRedirect(TOKEN_LOGIN_URL + "#error=%s" % e.message)

    # resolve which user model class should be used to lookup/create user
    UserModel = model_from_data(shibboleth_data)
    user_data = get_user_data(shibboleth_data)
    display_data = get_display_data(shibboleth_data)

    user = None
    token = None
    created = False

    if enable_login:
        enable_user = get_object_or_404(ApellaUser, pk=enable_login)
        key = auth_hooks.init_enable_shibboleth(
            enable_user, apella2_shibboleth_id, shibboleth_data)
        redirect_url = TOKEN_LOGIN_URL + "#enable-academic=%s" % key
        return HttpResponseRedirect(redirect_url)

    if old_apella_shibboleth_id and old_apella_shibboleth_id != "0":
        s_identifier = request.session.pop('shibboleth_id', None)
        if s_identifier != apella2_shibboleth_id:
            logger.error("forged migration")
            raise PermissionDenied("forged migration handshake")

        try:
            migration_key = request.session.pop('migration_key', None)
            with transaction.atomic():
                legacy = auth_hooks.migrate_legacy(
                    migration_key, old_apella_shibboleth_id, apella2_shibboleth_id)
                if legacy is None:
                    raise ValueError
        except ValueError:
            msg = 'migration.error'
            return HttpResponseRedirect(TOKEN_LOGIN_URL + "#error=%s" % msg)

        logger.info("legacy id %s migrated to %s", legacy, apella2_shibboleth_id)

    request.session.pop('shibboleth_id', None)
    request.session.pop('migration_key', None)

    try:
        user = UserModel.objects.get(
            user__shibboleth_id=apella2_shibboleth_id)

        if force_register:
            msg = "user.exists"
            return HttpResponseRedirect(TOKEN_LOGIN_URL + "#error=%s" % msg)

        # user not active
        if not user.user.is_active:
            msg = 'user.not.active'
            return HttpResponseRedirect(TOKEN_LOGIN_URL + "#error=%s" % msg)

        #if not user.user.email_verified:
            #msg = 'user.not.email_verified'
            #return HttpResponseRedirect(TOKEN_LOGIN_URL + "#error=%s" % msg)

        token = auth_hooks.login_user(user.user, request)
        user.user.remote_data = json.dumps(shibboleth_data)
        user.user.save()
        token = token.key

    except UserModel.DoesNotExist:

        if force_login and MIGRATE_LEGACY and not old_apella_shibboleth_id:
            migration_key = make_migration_key(apella2_shibboleth_id)
            request.session['shibboleth_id'] = apella2_shibboleth_id
            request.session['migration_key'] = migration_key
            params = {'migrate': 1, 'migration_key': migration_key}
            params_string = urllib.urlencode(params)
            target_path = LEGACY_PATH + "?" + params_string
            user_idp = request.META['HTTP_SHIB_IDENTITY_PROVIDER']
            params2 = {'SAMLDS': 1, 'target': target_path, 'entityID': user_idp}
            target_path2 = "/Shibboleth.sso/Login?" + urllib.urlencode(params2)
            url = urlparse.urljoin(LEGACY_URL, target_path2)
            logger.info("redirect to legacy shibboleth login url: %r" % url)
            return HttpResponseRedirect(url)

        if force_login:
            msg = "user.not.found"
            return HttpResponseRedirect(TOKEN_LOGIN_URL + "#error=%s" % msg)

        token = create_registration_token(
            apella2_shibboleth_id, user_data, shibboleth_data)
        created = True

    if created:
        data = urllib.quote(base64.b64encode(json.dumps(user_data)))
        remote_data = urllib.quote(base64.b64encode(json.dumps(display_data)))
        redirect_url = TOKEN_REGISTER_URL
        params = '?initial=%s&academic=1&remote_data=%s' % (data, remote_data)

        email = user_data.get('email', None)
        warn_legacy = False
        if email and OldUser.objects.filter(email=email).exists():
            warn_legacy = True
        if warn_legacy:
            params = params + "&warn_legacy=1"
        token_fragment = params + '#token=%s' % (token,)
    else:
        redirect_url = TOKEN_LOGIN_URL
        token_fragment = '#token=' + token

    redirect_url = redirect_url + token_fragment
    return HttpResponseRedirect(redirect_url)
