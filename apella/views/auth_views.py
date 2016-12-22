from django.db import transaction
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from djoser import views as djoser_views
from djoser import serializers as djoser_serializers
from djoser import signals as djoser_signals
from djoser import settings as djoser_settings
from rest_framework import mixins
from rest_framework.response import Response

from apella.loader import adapter
from apella import auth_hooks
from apella.models import ApellaUser, InstitutionManager, Professor, \
    Candidate, RegistrationToken
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import ValidationError
from django.utils.crypto import get_random_string


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
        return []

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        return obj

    def get_serializer_class(self):
        user = self.request.user
        resource = USER_ROLE_MODEL_RESOURCES[user.role]['resource']
        return adapter.get_serializer(resource)


class CustomLoginSerializer(djoser_serializers.LoginSerializer):

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        self.user = auth_hooks.authenticate_user(username=username,
            password=password)
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


class CustomActivationView(djoser_views.ActivationView):

    serializer_class = CustomActivationSerializer

    @transaction.atomic
    def action(self, serializer):
        auth_hooks.activate_user(serializer.user)
        serializer.user.save()
        djoser_signals.user_activated.send(
            sender=self.__class__, user=serializer.user, request=self.request)
        return Response(status=204)


class CustomLogoutView(djoser_views.LogoutView):
    pass


def make_registration_serializer(serializer):
    """
    Polymorphic registration serializer based on provided `serializer`
    """
    class RegistrationSerializer(serializer):

        def save(self, *args, **kwargs):
            save = super(RegistrationSerializer, self).save
            data = self.context['request'].data
            return auth_hooks.register_user(save, data, *args, **kwargs)

        def validate(self, attrs):
            validate = super(RegistrationSerializer, self).validate
            return auth_hooks.validate_new_user(validate, attrs)

    return RegistrationSerializer


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


    @transaction.atomic
    def create(self, request, *args, **kwargs):
        resend_email = request.data.get('resend_verification', None)
        if resend_email:
            return self.resend_verification(request, resend_email)

        user = request.data['user'];
        if not user:
            request.data['user'] = user = {}

        role = self.request.data.get('user_role', None)
        if not role or role not in USER_ROLE_MODEL_RESOURCES:
            raise ValidationError({"role": "invalid role"})

        request.data['user']['role'] = role

        token = request.data.get('registration_token', None)
        if token:
            token = get_object_or_404(RegistrationToken, token=token)
            user['username'] = token.identifier
            user['password'] = get_random_string(100)
            # TODO: extract token data to non-set request values

        return super(CustomRegistrationView, self).create(
            request, *args, **kwargs)

        return resp
