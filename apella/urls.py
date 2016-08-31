from django.conf.urls import patterns, url

from apella import views
from apella.views import UserListView

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^users/$', UserListView.as_view(), name='user-list'),
    url(r'^/users/(?P<user_id>\d+)/$', views.user_detail, name='user_detail'),
    url(r'^positions/$', views.position_list, name='position_list'),
    url(r'^/positions/(?P<position_id>\d+)/$',
        views.position_detail, name='position_detail'),

)
