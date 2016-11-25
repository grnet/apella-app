from django.apps import apps
from django.conf import settings
from django.shortcuts import get_object_or_404
from djoser import views as djoser_views

from apimas.modeling.adapters.drf import serializers
from apella.models import ApellaUser, InstitutionManager, Professor, \
        Candidate


class CustomLoginView(djoser_views.LoginView):
    pass


class CustomLogoutView(djoser_views.LogoutView):
    pass


def get_model_from_name(model_name):
    parts = model_name.split('.')
    model_name = parts[-1]
    model = apps.get_model(app_label='apella', model_name=model_name)
    return model


USER_ROLE_MODEL_RESOURCES = {
    'institutionmanager': {
        "model": InstitutionManager,
        "resource": "institution-managers"
    },
    'assistant': {
        "model": InstitutionManager,
        "resource": "institution-managers"
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
        model = USER_ROLE_MODEL_RESOURCES[user.role]['model']
        cls = serializers.generate(
                model,
                settings.API_SCHEMA_TMP['resources'][resource]['field_schema'])
        return cls
