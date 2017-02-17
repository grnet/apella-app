import os
import urlparse
from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import detail_route
from rest_framework.serializers import ValidationError

from django.db.models import ProtectedError, Min, Q
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.core.exceptions import MultipleObjectsReturned
from django.utils import timezone

from apimas.modeling.adapters.drf.mixins import HookMixin

from apella.models import InstitutionManager, Position, Department, \
    Candidacy, ApellaFile, ElectorParticipation, \
    OldApellaUserMigrationData, generate_filename, ApellaFileId
from apella.loader import adapter
from apella.common import FILE_KIND_TO_FIELD
from apella import auth_hooks
from apella.serializers.position import copy_candidacy_files
from apella.migration_functions import migrate_user_profile_files
from apella.emails import send_user_email

from apella.util import urljoin


class DestroyProtectedObject(viewsets.ModelViewSet):
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response(status=status.HTTP_403_FORBIDDEN)


class Professor(object):
    def get_queryset(self):
        queryset = self.queryset
        if 'ordering' not in self.request.query_params:
            queryset = self.queryset.order_by('user__last_name__el')
        return queryset


class AssistantList(generics.ListAPIView):
    def get_queryset(self):
        user = self.request.user
        if user.is_manager():
            institution_id = user.institutionmanager.institution_id
            return InstitutionManager.objects.filter(
                manager_role='assistant',
                institution__id=institution_id)
        else:
            return InstitutionManager.objects.filter(
                manager_role='assistant')

elector_sets = {
    'electors_regular_internal': True,
    'electors_regular_external': True,
    'electors_sub_internal': False,
    'electors_sub_external': False
}

committee_sets = ['committee_internal', 'committee_external']


class PositionHookMixin(HookMixin):
    def preprocess_update(self):
        obj = self.unstash()
        position = obj.instance
        ElectorParticipation.objects.filter(position=position).delete()
        for elector_set_key, is_regular in elector_sets.items():
            if elector_set_key in obj.validated_data:
                for elector in obj.validated_data[elector_set_key]:
                    if not ElectorParticipation.objects.filter(
                            professor=elector,
                            position=position,
                            is_regular=is_regular).exists():
                        ElectorParticipation.objects.create(
                            professor=elector,
                            position=position,
                            is_regular=is_regular)

        c = {'committee': []}
        for com_set in committee_sets:
            if com_set in obj.validated_data:
                committee = obj.validated_data[com_set]
                if committee:
                    for professor in committee:
                        c['committee'].append(professor)
        self.stash(extra=c)


class PositionMixin(object):

    @detail_route()
    def history(self, request, pk=None):
        position = self.get_object()
        position_states = Position.objects.filter(code=position.code)
        serializer = self.get_serializer(position_states, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if user.is_institutionmanager():
            queryset = queryset.filter(
                department__in=user.institutionmanager.
                institution.department_set.all())
        elif user.is_assistant():
            queryset = queryset.filter(
                department__in=user.institutionmanager.
                departments.all())
        elif user.is_professor():
            position_ids = Candidacy.objects.filter(
                candidate=user).values_list('position_id', flat=True)
            queryset = queryset.filter(
                Q(state='posted', ends_at__gte=datetime.now()) |
                Q(id__in=position_ids) |
                Q(committee=user.professor.id) |
                Q(electors=user.professor.id))
        elif user.is_candidate():
            position_ids = Candidacy.objects.filter(
                candidate=user).values_list('position_id', flat=True)
            queryset = queryset.filter(
                Q(state='posted', ends_at__gte=datetime.now()) |
                Q(id__in=position_ids))
        if 'pk' in self.kwargs:
            return queryset.filter(id=self.kwargs['pk'])
        else:
            ids = queryset.values('code').annotate(Min('id')). \
                values('id__min')
            return queryset.filter(id__in=ids)

    def update(self, request, *args, **kwargs):
        position = self.get_object()
        code = position.code
        if code.split(settings.POSITION_CODE_PREFIX)[1] != \
                str(position.id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super(PositionMixin, self).update(request, *args, **kwargs)


class CandidacyList(object):

    @detail_route()
    def history(self, request, pk=None):
        candidacy = self.get_object()
        candidacy_states = Candidacy.objects.filter(code=candidacy.code)
        serializer = self.get_serializer(candidacy_states, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if user.is_institutionmanager():
            institution_ids = InstitutionManager.objects.filter(user=user). \
                values_list('institution', flat=True)
            departments = Department.objects.filter(
                institution_id__in=institution_ids)
            positions = Position.objects.filter(department__in=departments)
            queryset = queryset.filter(position__in=positions)
        elif user.is_assistant():
            positions = Position.objects.filter(author_id=user.id)
            queryset = queryset.filter(position__in=positions)
        if 'pk' in self.kwargs:
            return queryset.filter(id=self.kwargs['pk'])
        else:
            ids = queryset.values('code').annotate(Min('id')).values('id__min')
            return queryset.filter(id__in=ids)

    def update(self, request, pk=None):
        candidacy = self.get_object()
        code = candidacy.code
        if code != str(candidacy.id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super(CandidacyList, self).update(request, pk=None)


class RegistriesList(viewsets.GenericViewSet):

    def get_queryset(self):
        queryset = self.queryset
        if 'ordering' not in self.request.query_params:
            queryset = queryset.order_by('department')
        else:
            ordering = self.request.query_params['ordering']
            queryset = queryset.order_by(ordering)
        return queryset

    @detail_route()
    def members(self, request, pk=None):
        registry = self.get_object()
        query_params = self.request.query_params
        members = registry.members
        if 'user_id' in query_params:
            members = members.filter(user_id=query_params['user_id'])
        if 'institution' in query_params:
            members = members.filter(institution=query_params['institution'])
        if 'rank' in query_params:
            members = members.filter(rank=query_params['rank'])
        if 'search' in query_params:
            search = query_params['search']
            members = members.filter(
                Q(user__last_name__en__icontains=search) |
                Q(user__last_name__el__icontains=search) |
                Q(discipline_text__icontains=search))
        if 'ordering' not in query_params:
            ordering = 'user__last_name__el'
        else:
            ordering = query_params['ordering']
        members = members.order_by(ordering)

        ser = adapter.get_serializer('professors')
        page = self.paginate_queryset(members)
        if page is not None:
            return self.get_paginated_response(
                ser(page, many=True, context={'request': request}).data)
        return Response(
            ser(members, many=True, context={'request': request}).data)


USE_X_SEND_FILE = getattr(settings, 'USE_X_SEND_FILE', False)


class FilesViewSet(viewsets.ModelViewSet):

    @detail_route(methods=['get', 'head'])
    def download(self, request, pk=None):
        response = HttpResponse(content_type='application/force-download')
        if request.method == 'HEAD':
            user = request.user
            file = get_object_or_404(ApellaFile, id=pk)
            if not file.check_user_can_download(user):
                raise Http404

            token = auth_hooks.generate_file_token(user, file)
            url = urljoin(settings.BASE_URL or '/',
                          reverse('apella-files-download', args=(pk,)))
            response['X-File-Location'] = "%s?token=%s" % (url, token)
            return response

        token = request.GET.get('token', None)
        if token is None:
            raise PermissionDenied("no.token")
            # url = reverse('apella-files-download', args=(pk,))
            # ui_url = getattr(settings, 'DOWNLOAD_FILE_URL', '')
            # ui_download_url = '%s?#download=%s' % (ui_url, url)
            # return HttpResponseRedirect(ui_download_url)

        file_id = auth_hooks.consume_file_token(user, token)
        if not file_id == pk:
            raise Http404

        file = get_object_or_404(ApellaFile, id=file_id)
        disp = 'attachment; filename=%s' % file.file_name
        response['Content-Disposition'] = disp
        if USE_X_SEND_FILE:
            response['X-Sendfile'] = file.file_content.path
        else:
            response.content = open(file.file_content.path)
        return response

    def destroy(self, request, pk=None):
        obj = self.get_object()
        try:
            f = os.path.join(settings.MEDIA_ROOT, obj.file_content.name)
            os.remove(f)
        except OSError:
            pass
        return super(FilesViewSet, self).destroy(request, pk)


class UploadFilesViewSet(viewsets.ModelViewSet):

    FILE_SOURCE = {
        "Professor": "profile",
        "Candidate": "profile",
        "Candidacy": "candidacy",
        "Position": "position",
        "Registry": "registry"
    }

    @detail_route(methods=['post'])
    def upload(self, request, pk=None):
        obj = self.get_object()
        if 'file_upload' not in request.FILES:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        file_upload = request.FILES['file_upload']
        file_kind = request.data['file_kind']
        file_description = request.data['file_description']

        if file_kind not in FILE_KIND_TO_FIELD:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not file_upload:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        field_name, many = FILE_KIND_TO_FIELD[file_kind].values()
        if field_name not in obj._meta.get_all_field_names():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        apella_file_id = ApellaFileId.objects.create()
        uploaded_file = ApellaFile.objects.create(
                owner=request.user,
                file_kind=file_kind,
                source=self.FILE_SOURCE[obj.__class__.__name__],
                source_id=obj.id,
                file_content=file_upload,
                file_name=file_upload.name,
                description=file_description,
                updated_at=timezone.now(),
                file_id=apella_file_id)

        if not many:
            setattr(obj, field_name, uploaded_file)
        else:
            many_attr = getattr(obj, field_name)
            many_attr.add(uploaded_file)
        obj.save()
        return Response(status=status.HTTP_200_OK)


class SyncCandidacies(object):
    @detail_route(methods=['post'])
    def sync_candidacies(self, request, pk=None):
        candidate_user = self.get_object()
        active_candidacies = Candidacy.objects.filter(
            candidate=candidate_user.user,
            state='posted',
            position__state='posted',
            position__ends_at__gt=datetime.now())
        for candidacy in active_candidacies:
            copy_candidacy_files(candidacy, candidate_user.user)
        return Response(request.data, status=status.HTTP_200_OK)


class CandidateProfile(object):
    @detail_route(methods=['post'])
    def request_verification(self, request, pk=None):
        candidate_user = self.get_object()
        try:
            auth_hooks.request_user_verify(candidate_user)
            candidate_user.save()
        except ValidationError as ve:
            return Response(ve.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(request.data, status=status.HTTP_200_OK)

    @detail_route(methods=['post'])
    def request_changes(self, request, pk=None):
        candidate_user = self.get_object()
        try:
            auth_hooks.request_user_changes(candidate_user)
            candidate_user.save()
            send_user_email(
                candidate_user.user,
                'apella/emails/user_profile_request_changes_subject.txt',
                'apella/emails/user_profile_request_changes_body.txt')
        except ValidationError as ve:
            return Response(ve.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(request.data, status=status.HTTP_200_OK)

    @detail_route(methods=['post'])
    def verify_user(self, request, pk=None):
        candidate_user = self.get_object()
        try:
            auth_hooks.verify_user(candidate_user)
            candidate_user.save()
            send_user_email(
                candidate_user.user,
                'apella/emails/user_verified_profile_subject.txt',
                'apella/emails/user_verified_profile_body.txt')
        except ValidationError as ve:
            return Response(ve.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(request.data, status=status.HTTP_200_OK)

    @detail_route(methods=['post'])
    def reject_user(self, request, pk=None):
        candidate_user = self.get_object()
        try:
            reason = None
            if 'rejected_reason' in request.data:
                reason = request.data['rejected_reason']
            auth_hooks.reject_user(candidate_user, reason=reason)
            candidate_user.save()
            send_user_email(
                candidate_user.user,
                'apella/emails/user_rejected_profile_subject.txt',
                'apella/emails/user_rejected_profile_body.txt')
        except ValidationError as ve:
            return Response(ve.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(request.data, status=status.HTTP_200_OK)

    @detail_route(methods=['post'])
    def migrate_user_profile_files(self, request, pk=None):
        candidate_user = self.get_object()
        if 'old_user_id' not in request.data:
            return Response(
                {"old_user_id": "old_user_id.required.error"},
                status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                old_user = OldApellaUserMigrationData.objects.get(
                    user_id=int(request.data['old_user_id']),
                    role=candidate_user.user.role)
            except OldApellaUserMigrationData.DoesNotExist as dne:
                return Response(
                    dne.message, status=status.HTTP_400_BAD_REQUEST)
            except MultipleObjectsReturned as mor:
                return Response(
                    mor.message, status=status.HTTP_400_BAD_REQUEST)
            # TODO remove current files, if exist
            migrate_user_profile_files(old_user, candidate_user.user)

        return Response(request.data, status=status.HTTP_200_OK)
