from django.conf.urls import patterns, url

from apella import views
from apella.views import UserListView, PositionListView, CandidacyListView

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^users/$', UserListView.as_view(), name='user-list'),
    url(r'^users/new/$', views.user_edit, name='user-new'),
    url(r'^users/(?P<user_id>\d+)/$', views.user_edit, name='user-edit'),
    url(r'^positions/$', PositionListView.as_view(), name='position-list'),
    url(r'^positions/new$', views.position_edit, name='position-new'),
    url(r'^positions/(?P<position_id>\d+)/edit/$',
        views.position_edit, name='position-edit'),
    url(r'^candidacies/$', CandidacyListView.as_view(), name='candidacy-list'),
    url(r'^candidacies/new/(?P<position_id>\d+)/$',
        views.candidacy_edit, name='candidacy-new'),
    url(r'^candidacies/(?P<candidacy_id>\d+)/edit/$',
        views.candidacy_edit, name='candidacy-edit'),

)
