from djoser import views as djoser_views


class CustomLoginView(djoser_views.LoginView):
    pass


class CustomLogoutView(djoser_views.LogoutView):
    pass


class CustomUserView(djoser_views.UserView):
    pass
