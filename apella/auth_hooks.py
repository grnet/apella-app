from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ValidationError
from django.contrib.auth import user_logged_in, user_logged_out
from apella.models import RegistrationToken


def validate_new_user(validate, attrs):
    return validate(attrs)


def register_user(save, data, *args, **kwargs):
    token = data.get('registration_token', None)
    if token:
        token = get_object_or_404(RegistrationToken, token=token)

    user = save(*args, **kwargs)
    user.user.is_active = False
    user.user.email_verified = False
    user.is_verified = False

    if token:
        user.user.shibboleth_id = token.identifier
        user.user.set_unusable_password()
        # TODO: we may consider automatically verify the user entry
        # only in case user has not modified shibboleth provided data
        user.is_verified = True
        token.delete()

    user.user.save()
    user.save()
    return user


def activate_user(user):
    user.email_verified = True
    user.is_active = True


def authenticate_user(**kwargs):
    return authenticate(**kwargs)


def validate_user_login(user, errors):
    if not user.is_active:
        key = 'inactive_account'
        raise ValidationError(errors.get(key, key))
    if not user.email_verified:
        key = 'email.not.verified'
        raise ValidationError(errors.get(key, key))
    if user.role == 'professor' and not user.professor.is_verified:
        key = 'user.not.moderated'
        raise ValidationError(errors.get(key, key))
    return user


def login_user(user, request=None):
    token, _ = Token.objects.get_or_create(user=user)
    user_logged_in.send(sender=user.__class__, request=request, user=user)
    return token


def logout_user(user, request=None):
    Token.objects.filter(user=request.user).delete()
    user_logged_out.send(
        sender=request.user.__class__, request=request, user=request.user)
    return user
