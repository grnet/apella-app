from django.shortcuts import get_object_or_404
from djoser import views as djoser_views
from rest_framework import mixins

from apella.loader import adapter
from apella.models import ApellaUser, InstitutionManager, Professor, \
    Candidate, RegistrationToken
from django.core.exceptions import ValidationError, PermissionDenied
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


class CustomLoginView(djoser_views.LoginView):
    pass


class CustomLogoutView(djoser_views.LogoutView):
    pass


class CustomRegistrationView(djoser_views.RegistrationView,
                             mixins.UpdateModelMixin):

    def get_serializer_class(self):
        role = self.request.data.get('user_role', None)
        if not role or role not in USER_ROLE_MODEL_RESOURCES:
            raise ValidationError({"role": "invalid role"})

        resource = USER_ROLE_MODEL_RESOURCES[role]['resource']
        return api_serializers.get(resource)

    def create(self, request, *args, **kwargs):
        key = self.request.data.get('registration_token', None)
        token = None
        user = request.data['user'];
        if not user:
            request.data['user'] = user = {}

        if key:
            token = get_object_or_404(RegistrationToken, token=key)
            user['username'] = token.identifier
            user['password'] = get_random_string(100)
            user['shibboleth_id'] = token.identifier
            # TODO: extract token data to non-set request values

        resp = super(CustomRegistrationView, self).create(
            request, *args, **kwargs)

        if token:
            user = ApellaUser.objects.get(username=token.identifier)
            user.shibboleth_id = token.identifier
            user.set_unusable_password()
            user.save()
            token.delete()

        return resp
