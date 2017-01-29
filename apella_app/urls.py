from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include
from django.views.generic.base import RedirectView

from apella.views import auth_views
from apella.views import shibboleth_views
from apella import views
from apella.loader import api_urls

admin.autodiscover()


api_prefix = settings.API_PREFIX
apipatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/auth/register/$',
        auth_views.CustomRegistrationView.as_view(), name='register'),
    url(r'^api/auth/activate/$',
        auth_views.CustomEmailVerificationView.as_view(), name='activate'),
    url(r'^api/auth/password/$',
        auth_views.CustomPasswordView.as_view(), name='set_password'),
    url(r'^api/auth/password-reset/$',
        auth_views.CustomPasswordResetView.as_view(), name='reset_password'),
    url(r'^api/auth/password-reset/confirm/$',
        auth_views.CustomPasswordResetConfirmView.as_view(),
        name='reset_password_confirm'),
    url(r'^api/auth/login/$',
        auth_views.CustomLoginView.as_view(), name='login'),
    url(r'^api/auth/logout/$',
        auth_views.CustomLogoutView.as_view(), name='logout'),
    url(r'^api/auth/me/$', auth_views.CustomUserView.as_view(), name='user'),
    url(r'^api/config.json$', views.config, name='config'),
    url(r'^api/shibboleth$', shibboleth_views.login, name='shibboleth_login'),
    url(r'^api/shibboleth-legacy$', shibboleth_views.legacy_login, name='shibboleth_legacy'),
    api_urls
]

urlpatterns = [
    url(api_prefix, include(apipatterns))
]

ui_prefix = getattr(settings, 'UI_PREFIX', 'apella/ui/')
if ui_prefix and ui_prefix != '/':
    urlpatterns += [
        url('^$', RedirectView.as_view(url=ui_prefix))
    ]

if getattr(settings, 'SERVE_UI', True):
    # make django app serve ember dist files
    from django.conf.urls.static import static
    from django.views.static import serve
    from os import path

    root = path.dirname(__file__)
    ui_root = path.abspath(path.join(root, '..', '..', 'apella/ui/dist'))

    # admin may optionaly use a custom dist dir via settings
    ui_root = getattr(settings, 'UI_ROOT', ui_root)
    assets = path.join(ui_root, 'assets')

    # this should match ember application baseURL setting
    urlpatterns += static('%sassets/' % ui_prefix, document_root=assets)

    # serve index.html for all paths
    urlpatterns += [
        url('^%s.*' % ui_prefix, serve, {
            'path': 'index.html',
            'document_root': ui_root
            }),
    ]
