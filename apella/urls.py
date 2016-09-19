from django.conf.urls import patterns, url

from apella import views
from apella.views import *

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^users/$', UserListView.as_view(), name='user-list'),
    url(r'^users/new/$', views.user_edit, name='user-new'),
    url(r'^users/(?P<user_id>\d+)/$', views.user_edit, name='user-edit'),
    url(r'^positions/$', PositionListView.as_view(), name='position-list'),
    url(r'^positions/([\w-]+)/$',
        PositionListView.as_view(), name='position-list'),
    url(r'^positions/new$', views.position_edit, name='position-new'),
    url(r'^positions/(?P<position_id>\d+)/edit/$',
        views.position_edit, name='position-edit'),
    url(r'^candidacies/$', CandidacyListView.as_view(), name='candidacy-list'),
    url(r'^candidacies/([\w-]+)/$',
        CandidacyListView.as_view(), name='candidacy-list'),
    url(r'^candidacies/new/(?P<position_id>\d+)/$',
        views.candidacy_edit, name='candidacy-new'),
    url(r'^candidacies/(?P<candidacy_id>\d+)/edit/$',
        views.candidacy_edit, name='candidacy-edit'),
    url(r'^institutions/$',
        InstitutionListView.as_view(), name='institution-list'),
    url(r'^institutions/new/$',
        views.institution_edit, name='institution-new'),
    url(r'^institutions/(?P<institution_id>\d+)/$',
        views.institution_edit, name='institution-edit'),
    url(r'^departments/$',
        DepartmentListView.as_view(), name='department-list'),
    url(r'^departments/new/$', views.department_edit, name='department-new'),
    url(r'^departments/(?P<department_id>\d+)/$',
        views.department_edit, name='department-edit'),
    url(r'^subject_areas/$',
        SubjectAreaListView.as_view(), name='subject-area-list'),
    url(r'^subject_areas/new/$', views.subject_area_edit,
        name='subject-area-new'),
    url(r'^subject_areas/(?P<subject_area_id>\d+)/$',
        views.subject_area_edit, name='subject-area-edit'),
    url(r'^subjects/$',
        SubjectListView.as_view(), name='subject-list'),
    url(r'^subjects/new/$', views.subject_edit,
        name='subject-new'),
    url(r'^subjects/(?P<subject_id>\d+)/$',
        views.subject_edit, name='subject-edit'),

)
