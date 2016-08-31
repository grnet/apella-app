from django.conf.urls import patterns, url

from apella import views
from apella.views import UserListView, PositionListView

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^users/$', UserListView.as_view(), name='user-list'),
    url(r'^users/(?P<user_id>\d+)/$', views.user_detail, name='user-detail'),
    url(r'^positions/$', PositionListView.as_view(), name='position-list'),
    url(r'^positions/new$', views.position_edit, name='position-new'),
    url(r'^positions/(?P<position_id>\d+)/edit/$',
        views.position_edit, name='position-edit'),

)
