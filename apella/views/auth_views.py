from django.utils.importlib import import_module
from django.conf import settings
from djoser import views as djoser_views


USER_ROLE_MODEL_RESOURCES = {
    'institutionmanager': {
        "resource": "institution-managers"
    },
    'assistant': {
        "resource": "institution-managers"
    },
    'candidate': {
        "resource": "candidates"
    },
    'professor': {
        "resource": "professors"
    },
    'helpdeskuser': {
        "resource": "users"
    },
    'helpdeskadmin': {
        "resource": "users"
    }
}


class CustomUserView(djoser_views.UserView):

    def get_serializer_class(self):
        user = self.request.user
        resource = USER_ROLE_MODEL_RESOURCES[user.role]['resource']
        urls = import_module(settings.ROOT_URLCONF)
        ser = urls.serializers.get(resource)
        return ser


class CustomLoginView(djoser_views.LoginView):
    pass


class CustomLogoutView(djoser_views.LogoutView):
    pass
