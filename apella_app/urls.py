from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include
from django.views.generic.base import RedirectView

from apimas.modeling.adapters.drf import django_rest
from apimas.modeling.cli.cli import load_config
from apella.views import auth_views


admin.autodiscover()
config = load_config()
adapter = django_rest.DjangoRestAdapter()
adapter.construct(config.get('spec'))
adapter.apply()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/auth/login/$',
        auth_views.CustomLoginView.as_view(), name='login'),
    url(r'^api/auth/logout/$',
        auth_views.CustomLogoutView.as_view(), name='logout'),
    url(r'^api/auth/me/$', auth_views.CustomUserView.as_view(), name='user'),
    adapter.urls
]

ui_prefix = getattr(settings, 'UI_PREFIX', 'ui/')
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
