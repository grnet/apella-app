import os
import logging
from datetime import datetime, date, time

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import detail_route
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import PermissionDenied

from django.db.models import ProtectedError, Min, Q, Max
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from apimas.modeling.adapters.drf.mixins import HookMixin

from apella.models import InstitutionManager, Position, Department, \
    Candidacy, ApellaFile, ElectorParticipation, Candidate, \
    Professor as ProfessorModel
from apella.loader import adapter
from apella.common import FILE_KIND_TO_FIELD
from apella import auth_hooks
from apella.serializers.position import link_files, \
    upgrade_candidate_to_professor
from apella.emails import send_user_email, send_emails_file, \
    send_emails_members_change
from apella.util import urljoin, safe_path_join
from apella.serials import get_serial

logger = logging.getLogger(__name__)

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
        create_registry = self.request.query_params.get(
            'create_registry', None)
        if create_registry:
            queryset = queryset.exclude(rank='Lecturer'). \
                exclude(rank='Tenured Assistant Professor')
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

        eps = ElectorParticipation.objects.filter(position=position)
        old_participations = [old_el_pa for old_el_pa in eps.all()]
        eps.all().delete()

        new_participations = []
        for elector_set_key, is_regular in elector_sets.items():
            if elector_set_key in obj.validated_data:
                for elector in obj.validated_data[elector_set_key]:
                    ep = ElectorParticipation.objects.create(
                        professor=elector,
                        position=position,
                        is_regular=is_regular,
                        is_internal=elector_set_key.endswith('internal'))
                    new_participations.append(ep)

        send_emails_members_change(
            position, 'electors', {'e': old_participations},
            {'e': new_participations})

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
        now = datetime.utcnow()
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
            position_ids = list(Candidacy.objects.filter(
                candidate=user).values_list('position_id', flat=True))
            if user.professor.department:
                department_position_ids = list(Position.objects.filter(
                    department=user.professor.department).
                    values_list('id', flat=True))
                position_ids += department_position_ids
            queryset = queryset.filter(
                Q(state='posted', ends_at__gte=now) |
                Q(id__in=position_ids) |
                Q(committee=user.professor.id) |
                Q(electors=user.professor.id))
        elif user.is_candidate():
            position_ids = Candidacy.objects.filter(
                candidate=user).values_list('position_id', flat=True)
            queryset = queryset.filter(
                Q(state='posted', ends_at__gte=now) |
                Q(id__in=position_ids))
        if 'pk' in self.kwargs:
            queryset = queryset.filter(id=self.kwargs['pk'])
        else:
            ids = queryset.values('code').annotate(Min('id')). \
                values('id__min')
            queryset = queryset.filter(id__in=ids)

        state_query = self.request.GET.get('state_expanded')
        if state_query:
            now = datetime.utcnow()
            if state_query in ('electing', 'successful',
                               'failed', 'cancelled', 'revoked'):
                queryset = queryset.filter(Q(state=state_query))

            elif state_query == 'posted':
                queryset = queryset.filter(Q(state='posted') &
                                           Q(starts_at__gte=now))

            elif state_query == 'open':
                queryset = queryset.filter(Q(state='posted') &
                                           Q(starts_at__lte=now) &
                                           Q(ends_at__gt=now))
            elif state_query == 'closed':
                queryset = queryset.filter(Q(state='posted') &
                                           Q(ends_at__lte=now))

            elif state_query == 'before_closed':
                queryset = queryset.filter(Q(state='posted') &
                                           Q(ends_at__gt=now))
        queryset = queryset.distinct()
        return queryset

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
            departments = user.institutionmanager.departments.all()
            positions = Position.objects.filter(department__in=departments)
            queryset = queryset.filter(position__in=positions)
        if 'pk' in self.kwargs:
            queryset = queryset.filter(id=self.kwargs['pk'])
        else:
            ids = queryset.values('code').annotate(Min('id')). \
                values_list('id__min', flat=True)
            queryset = queryset.filter(id__in=ids)
            if 'latest' in self.request.query_params:
                q2 = queryset.values('candidate', 'position').annotate(Max('id')). \
                    values_list('id__max', flat=True)
                queryset = queryset.filter(id__in=q2)
        if not user.is_helpdesk():
            queryset = queryset.exclude(state='draft')

        queryset = queryset.distinct()
        return queryset

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

    @detail_route(methods=['head'], url_path='download')
    def download_head(self, request, pk=None):
        response = HttpResponse(content_type='application/force-download')
        assert request.method == 'HEAD'
        user = request.user
        file = self.get_object()
        token = auth_hooks.generate_file_token(user, file)
        url = urljoin(settings.BASE_URL or '/',
                      reverse('apella-files-downloadfile', args=(pk,)))
        response['X-File-Location'] = "%s?token=%s" % (url, token)
        return response

    @detail_route(methods=['get'], url_path='downloadfile')
    def download_get(self, request, pk=None):
        response = HttpResponse(content_type='application/force-download')
        token = request.GET.get('token', None)
        if token is None:
            raise PermissionDenied("no.token")
            # url = reverse('apella-files-download', args=(pk,))
            # ui_url = getattr(settings, 'DOWNLOAD_FILE_URL', '')
            # ui_download_url = '%s?#download=%s' % (ui_url, url)
            # return HttpResponseRedirect(ui_download_url)

        file_id = auth_hooks.consume_file_token(token)
        if not file_id == int(pk):
            raise Http404

        file = get_object_or_404(ApellaFile, id=file_id)
        filename = file.file_name
        if isinstance(filename, unicode):
            filename = filename.encode('utf-8')
        filename = filename.replace('"', '')
        disp = 'attachment; filename="%s"' % filename
        response['Content-Disposition'] = disp
        if USE_X_SEND_FILE:
            response['X-Sendfile'] = file.file_content.path
        else:
            response.content = open(file.file_content.path)
        return response

    def destroy(self, request, pk=None):
        obj = self.get_object()
        try:
            f = safe_path_join(settings.MEDIA_ROOT, obj.file_content.name)
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
        file_upload = request.FILES.get('file_upload', None)
        file_kind = request.data.get('file_kind', None)
        file_description = request.data.get('file_description', None)

        if file_kind not in FILE_KIND_TO_FIELD:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not file_upload:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        field_name, many = FILE_KIND_TO_FIELD[file_kind].values()
        if field_name not in obj._meta.get_all_field_names():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        owner = request.user
        if request.user.is_helpdesk():
            if isinstance(obj, ProfessorModel) or isinstance(obj, Candidate):
                owner = obj.user
            elif isinstance(obj, Candidacy):
                owner = obj.candidate
            elif isinstance(obj, Position):
                owner = obj.author.user

        uploaded_file = ApellaFile.objects.create(
                id=get_serial('apella_file'),
                owner=owner,
                file_kind=file_kind,
                source=self.FILE_SOURCE[obj.__class__.__name__],
                source_id=obj.id,
                file_content=file_upload,
                file_name=file_upload.name,
                description=file_description,
                updated_at=datetime.utcnow())

        if not many:
            setattr(obj, field_name, uploaded_file)
        else:
            many_attr = getattr(obj, field_name)
            many_attr.add(uploaded_file)
        obj.save()
        send_emails_file(obj, file_kind)

        return Response(status=status.HTTP_200_OK)


class SyncCandidacies(object):
    @detail_route(methods=['post'])
    def sync_candidacies(self, request, pk=None):
        now = datetime.utcnow()
        candidate_user = self.get_object()
        active_candidacies = Candidacy.objects.filter(
            candidate=candidate_user.user,
            state='posted',
            position__state='posted',
            position__ends_at__gt=now)
        for candidacy in active_candidacies:
            link_files(candidacy, candidate_user.user)
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
    def upgrade_to_professor(self, request, pk=None):
        candidate_user = self.get_object()
        if not candidate_user.is_candidate():
            return Response(
                'not.a.candidate', status=status.HTTP_400_BAD_REQUEST)

        department = request.data.get('department', None)
        rank = request.data.get('rank', None)
        fek = request.data.get('fek', None)
        discipline_text = request.data.get('discipline_text', None)
        discipline_in_fek = request.data.get('discipline_in_fek', None)

        try:
            upgrade_candidate_to_professor(
                candidate_user.user,
                department=department,
                rank=rank,
                fek=fek,
                discipline_text=discipline_text,
                discipline_in_fek=discipline_in_fek)
        except ValidationError as ve:
            return Response(ve.detail, status=status.HTTP_400_BAD_REQUEST)
        return Response(request.data, status=status.HTTP_200_OK)
