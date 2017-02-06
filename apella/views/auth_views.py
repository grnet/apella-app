import hashlib

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from djoser import views as djoser_views
from djoser import serializers as djoser_serializers
from djoser import signals as djoser_signals
from djoser import settings as djoser_settings
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import ValidationError

from apella.loader import adapter
from apella import auth_hooks
from apella.models import ApellaUser, InstitutionManager, Professor, \
    Candidate, RegistrationToken, OldApellaUserMigrationData
from apella.migration_functions import migrate_username


USER_ROLE_MODEL_RESOURCES = {
    'institutionmanager': {
        "model": InstitutionManager,
        "resource": "institution-managers"
    },
    'assistant': {
        "model": InstitutionManager,
        "resource": "assistants"
    },
    'candidate': {
        "model": Candidate,
        "resource": "candidates"
    },
    'professor': {
        "model": Professor,
        "resource": "professors"
    },
    'helpdeskuser': {
        "model": ApellaUser,
        "resource": "users"
    },
    'helpdeskadmin': {
        "model": ApellaUser,
        "resource": "users"
    }
}


class CustomUserView(djoser_views.UserView):

    def get_queryset(self):
        user = self.request.user
        model = USER_ROLE_MODEL_RESOURCES[user.role]['model']
        if model is ApellaUser:
            return ApellaUser.objects.filter(id=user.id)
        if model.objects.filter(user_id=user.id).exists():
            return model.objects.filter(user_id=user.id)
        return model.objects.none()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        return obj

    def get_serializer_class(self):
        user = self.request.user
        resource = USER_ROLE_MODEL_RESOURCES[user.role]['resource']
        return adapter.get_serializer(resource)

    @transaction.atomic
    def _enable_academic(self, request, *args, **kwargs):
        user = request.user
        token = request.data.get('token', None)
        if not user or not token:
            raise PermissionDenied
        user = auth_hooks.consume_enable_shibboleth_token(token, user)
        if user:
            return HttpResponse(status=202)
        raise ValidationError({"non_field_errors": "generic.error"})

    def update(self, request, *args, **kwargs):
        user = self.get_object()

        if request.GET.get('enable_academic', False):
            return self._enable_academic(request, *args, **kwargs)

        if hasattr(user, 'verification_pending') and user.verification_pending:
            raise PermissionDenied("user.pending.verification")

        if hasattr(user, 'is_verified') and \
                user.is_verified and not user.user.is_assistant():
            raise PermissionDenied("user.verified")

        return super(CustomUserView, self).update(request, *args, **kwargs)


class CustomLoginSerializer(djoser_serializers.LoginSerializer):

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        self.user = auth_hooks.authenticate_user(
            username=username, password=password)
        if self.user:
            auth_hooks.validate_user_login(self.user, self.error_messages)
        else:
            raise ValidationError(self.error_messages['invalid_credentials'])
        return attrs


class CustomLoginView(djoser_views.LoginView):
    serializer_class = CustomLoginSerializer


class CustomActivationSerializer(djoser_serializers.ActivationSerializer):

    def validate(self, attrs):
        attrs = super(
            djoser_serializers.ActivationSerializer, self).validate(attrs)
        if self.user.email_verified:
            raise PermissionDenied(self.error_messages['stale_token'])
        return attrs


class CustomEmailVerificationView(djoser_views.ActivationView):
    """
    For djoser this view both verifies user email and activates user account.

    For Apella this is the case just for a set of users as there are cases for
    which we permit user activation, with grant to constrained access after login
    (profile edit), prior to email verification.
    """

    serializer_class = CustomActivationSerializer

    @transaction.atomic
    def action(self, serializer):
        should_activate = not bool(serializer.user.activated_at)
        auth_hooks.verify_email(serializer.user, should_activate)
        serializer.user.save()
        if should_activate:
            djoser_signals.user_activated.send(
                sender=self.__class__, user=serializer.user,
                request=self.request)
        return Response(status=204)


class CustomPasswordView(djoser_views.SetPasswordView):

    def post(self, request):
        if request.user and hasattr(request.user, 'login_method'):
            if request.user.login_method != 'password':
                raise PermissionDenied(
                    {"non_field_errors": "no.password.user"})
        return super(CustomPasswordView, self).post(request)


class CustomPasswordResetConfirmView(djoser_views.PasswordResetConfirmView):
    pass


class CustomPasswordResetView(djoser_views.PasswordResetView):

    def get_users(self, email):
        active_users = ApellaUser.objects.filter(
            email__iexact=email,
            is_active=True,
            login_method__iexact='password'
        )
        if len(active_users):
            return active_users

        active_old_users = OldApellaUserMigrationData.objects.filter(
            email__iexact=email,
            migrated_at=None,
            shibboleth_id=''
        )

        if not len(active_users) and not len(active_old_users):
            raise PermissionDenied({"email": "password.user.not.found"})

        new_user = migrate_username(active_old_users[0].username)
        return [new_user]


class CustomLogoutView(djoser_views.LogoutView):
    pass


def make_registration_serializer(serializer):
    """
    Polymorphic registration serializer based on provided `serializer`
    """
    class RegistrationSerializer(serializer.model_ser_cls):

        def save(self, *args, **kwargs):
            save = super(RegistrationSerializer, self).save
            data = self.context['request'].data
            return auth_hooks.register_user(save, data, *args, **kwargs)

        def validate(self, attrs):
            validate = super(RegistrationSerializer, self).validate
            return auth_hooks.validate_new_user(validate, attrs)

    class Serializer(serializer):
        model_ser_cls = RegistrationSerializer

    return Serializer


class CustomRegistrationView(djoser_views.RegistrationView,
                             mixins.UpdateModelMixin):

    def get_serializer_class(self):
        role = self.request.data.get('user_role', None)
        if not role or role not in USER_ROLE_MODEL_RESOURCES:
            raise ValidationError({"role": "invalid role"})

        resource = USER_ROLE_MODEL_RESOURCES[role]['resource']
        return make_registration_serializer(adapter.get_serializer(resource))

    def get_email_context(self, user):
        if not isinstance(user, ApellaUser):
            user = user.user
        return super(CustomRegistrationView, self).get_email_context(user)

    def resend_verification(self, request, email):
        try:
            user = ApellaUser.objects.get(email=email, email_verified=False)
        except ApellaUser.DoesNotExist:
            raise PermissionDenied("user.invalid.or.activated")

        if djoser_settings.get('SEND_ACTIVATION_EMAIL'):
            self.send_email(**self.get_send_email_kwargs(user))
        return HttpResponse(status=202)


    def perform_create(self, serializer):
        instance = serializer.save()
        djoser_signals.user_registered.send(
            sender=self.__class__, user=instance.user, request=self.request)
        if djoser_settings.get('SEND_ACTIVATION_EMAIL') \
                and not instance.user.email_verified:
            self.send_email(**self.get_send_email_kwargs(instance.user))

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        resend_email = request.data.get('resend_verification', None)
        if resend_email:
            return self.resend_verification(request, resend_email)

        user = request.data['user']
        if not user:
            request.data['user'] = user = {}

        role = self.request.data.get('user_role', None)
        if not role or role not in USER_ROLE_MODEL_RESOURCES:
            raise ValidationError({"role": "invalid role"})

        request.data['user']['role'] = role

        token = request.data.get('registration_token', None)
        if token:
            get_object_or_404(RegistrationToken, token=token)
            user['username'] = hashlib.md5(token).hexdigest()[:30]
            user['password'] = get_random_string(100)
            # TODO: extract token data to non-set request values

        return super(CustomRegistrationView, self).create(
            request, *args, **kwargs)
