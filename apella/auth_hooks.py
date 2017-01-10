import logging
import uuid

from datetime import datetime

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth import user_logged_in, user_logged_out
from django.core.cache import cache
from django.conf import settings

from rest_framework.authtoken.models import Token
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import PermissionDenied

from apella.models import RegistrationToken, ApellaUser

logger = logging.getLogger(__name__)


def validate_new_user(validate, attrs):
    """
    Validate data used to create a new user. This hook is called
    prior to creating the new user entry.

    validate: The serializer `validate` method of the resolved signup
              serializer.
    attrs: Requested user attributes

    Return::
        Validated data or raise a ValidationError
    """
    return validate(attrs)


def register_user(save, data, *args, **kwargs):
    """
    Create a new user record.

    save: Serializer `save` method
    data: The raw request data
    kwargs: The request data as sanitized by the serializer

    Return::
        Created user (Professor, Candidate etc.) instance.
    """
    token = data.get('registration_token', None)
    if token:
        token = get_object_or_404(RegistrationToken, token=token)

    # TODO: validate role / fields
    user = save(*args, **kwargs)
    user.user.is_active = False
    user.user.email_verified = False
    user.is_verified = False

    if token:
        user.user.shibboleth_id = token.identifier
        user.user.set_unusable_password()
        # TODO: we may consider automatically verify the user entry
        # only in case user has not modified shibboleth provided data
        try:
            validate_user_can_verify(user)
            verify_user(user)
        except ValidationError, e:
            logger.error("user %r is not valid for automatic verification %r",
                         user, e)
        token.delete()

    user.user.save()
    user.save()
    return user


def activate_user(user):
    """
    Logic which gets executed when user visits the email verification url.
    """
    user.email_verified = True
    user.is_active = True
    user.activated_at = datetime.now()


def authenticate_user(**kwargs):
    """
    Resolve user object based on post'ed credentials.
    """
    return authenticate(**kwargs)


def validate_user_login(user, errors):
    """
    Validate tha authenticated user is eligible to login.
    """
    if not user.email_verified:
        key = 'email.not.verified'
        raise ValidationError(errors.get(key, key))
    if not user.is_active:
        key = 'inactive_account'
        raise ValidationError(errors.get(key, key))
    return user


def login_user(user, request=None):
    """
    Once user is validated, issue a token.
    """
    token, _ = Token.objects.get_or_create(user=user)
    user_logged_in.send(sender=user.__class__, request=request, user=user)
    return token


def logout_user(user, request=None):
    """
    Logic which takes place when user asks to logout from the app.
    """
    Token.objects.filter(user=request.user).delete()
    user_logged_out.send(
        sender=request.user.__class__, request=request, user=request.user)
    return user


def init_legacy_migration(legacy_id, migration_key):
    """
    User authenticated to the shibboleth endpoint of legacy SP. If a legacy
    user exists, tag the entry with the migration_key. If no legacy user
    is found return None to redirect user to the new service signup.

    legacy_id: Legacy SP shibboleth identifier (targetedid or eppn or ...)
    migration_key: The migration session identifier

    Should return an identifier which will be used to migrate the legacy
    record.
    """
    try:
        user = ApellaUser.objects.get(shibboleth_id_legacy=legacy_id)
        user.shibboleth_migration_key = migration_key
        user.save()
    except ApellaUser.DoesNotExist:
        return None
    return user.id


def migrate_legacy(migration_key, migrate_id, shibboleth_id):
    """
    A user which previously authenticated to the legacy SP endpoint is
    now rederected to re-authenticate to the new SP shibboleth endpoint.

    migration_key: The key stored to the user session
    migrate_id: The legacy record identifier
    shibboleth_id: The new SP shibboleth identifier (targetedid or ....)
    """
    user = get_object_or_404(
        ApellaUser, id=migrate_id, shibboleth_migration_key=migration_key)
    user.shibboleth_id = shibboleth_id
    user.shibboleth_migration_key = None
    legacy = user.shibboleth_id_legacy
    user.shibboleth_id_legacy = None
    user.save()
    return legacy


def validate_user_can_verify(user):
    # validate that current user can request account verification
    if user.user.is_professor():
        if not user.cv_id and not user.cv_url:
            raise ValidationError({"non_field_errors": "cv.required.error"})

    if user.user.is_candidate():
        if not user.cv_id:
            raise ValidationError({"cv": "cv.required.error"})

    #TODO: include additional validations


def request_user_verify(user):
    validate_user_can_verify(user)
    user.verification_pending = True
    user.verification_request = datetime.now()


def verify_user(user):
    user.is_verified = True
    user.verified_at = datetime.now()
    user.verification_pending = False


FILE_TOKEN_TIMEOUT = getattr(settings, 'FILE_TOKEN_TIMEOUT', 60)
def validate_file_access(user, file):
    return True


def generate_file_token(user, file):
    if not user.is_authenticated():
        raise PermissionDenied()

    validate_file_access(user, file)

    cache_key = str(uuid.uuid4())
    cache_value = file.pk
    cache.set(cache_key, cache_value, FILE_TOKEN_TIMEOUT)
    return cache_key


def consume_file_token(user, file, token):
    file_id = cache.get(token)
    if not file_id or file_id != file.pk:
        raise PermissionDenied()
    validate_file_access(user, file)
    cache.delete(token)

