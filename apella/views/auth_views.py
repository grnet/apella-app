from django.shortcuts import get_object_or_404
from djoser import views as djoser_views

from apella.loader import adapter
from apella.models import ApellaUser, InstitutionManager, Professor, \
    Candidate

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
