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
from apella.models import OldApellaUserMigrationData as OldUser
from apella.migration_functions import migrate_username, migrate_shibboleth_id

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
        user.user.login_method = 'academic'
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
    user = authenticate(**kwargs)
    if user:
        return user

    if user is None:
        username = kwargs.get('username', None)
        password = kwargs.get('password', None)

        if ApellaUser.objects.filter(username=username).exists():
            return None

        try:
            old_users = OldUser.objects.filter(username=username)
        except OldUser.DoesNotExist:
            return None

        password_valid = False
        for old_user in old_users:
            try:
                old_user.check_password(password)
                password_valid = True
            except ValueError:
                pass

        if password_valid:
            user = migrate_username(username, password)
            if user:
                return authenticate(**kwargs)
            return None


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
    old_user = OldUser.objects.filter(shibboleth_id=legacy_id)
    if old_user.exists():
        old_user = old_user[0]
    else:
        return None
    old_user.migration_key = migration_key
    old_user.save()
    return old_user.id


def migrate_legacy(migration_key, migrate_id, shibboleth_id):
    """
    A user which previously authenticated to the legacy SP endpoint is
    now rederected to re-authenticate to the new SP shibboleth endpoint.

    migration_key: The key stored to the user session
    migrate_id: The legacy record identifier
    shibboleth_id: The new SP shibboleth identifier (targetedid or ....)
    """
    old_user = get_object_or_404(
        OldUser, id=migrate_id, migration_key=migration_key)
    user = migrate_shibboleth_id(old_user.shibboleth_id)
    if not user:
        old_user.migration_key = None
        old_user.save()
        return None

    user.shibboleth_id = shibboleth_id
    user.shibboleth_migration_key = migration_key
    user.login_method = 'academic'
    user.save()
    return old_user.shibboleth_id


def validate_user_can_verify(user):
    # validate that current user can request account verification
    if user.user.is_professor():
        if not user.cv_professor and not user.cv_url:
            raise ValidationError({"non_field_errors": "cv.required.error"})
        if not user.rank:
            raise ValidationError({"rank": "rank.required.error"})
        if user.user.is_foreign_professor():
            if not user.institution_freetext:
                raise ValidationError(
                    {"institution_freetext":
                        "institution_freetext.required.error"})

        else:
            if not user.institution:
                raise ValidationError(
                    {"institution": "institution.required.error"})
            if not user.department:
                raise ValidationError(
                    {"department": "department.required.error"})
            if not user.fek:
                raise ValidationError(
                    {"fek": "fek.required.error"})
            if not user.discipline_in_fek and not user.discipline_text:
                raise ValidationError(
                    {"non_field_errors": "discipline.required.error"})


    if user.user.is_candidate():
        if not user.id_passport_file:
            raise ValidationError({"id_passport_file":
                "id_passport_file.required.error"})


def request_user_verify(user):
    validate_user_can_verify(user)
    user.verification_pending = True
    user.verification_request = datetime.now()


def verify_user(user):
    user.is_verified = True
    user.verified_at = datetime.now()
    user.verification_pending = False
    user.is_rejected = False


def reject_user(user, reason=None):
    user.is_verified = False
    user.is_rejected = True
    user.verification_pending = False
    if reason:
        user.rejected_reason = reason


def request_user_changes(user):
    user.verification_pending = False
    user.changes_request = datetime.now()


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

