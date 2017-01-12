import urlparse

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import detail_route

from django.db.models import ProtectedError, Min, Q
from django.conf import settings
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404


from apimas.modeling.adapters.drf.mixins import HookMixin

from apella.models import InstitutionManager, Position, Department, \
        Candidacy, ApellaUser, ApellaFile, ElectorParticipation
from apella.loader import adapter
from apella.common import FILE_KINDS, FILE_KIND_TO_FIELD
from apella import auth_hooks


class DestroyProtectedObject(viewsets.ModelViewSet):
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response(status=status.HTTP_403_FORBIDDEN)


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
        if user.is_manager():
            institution_ids = InstitutionManager.objects.filter(user=user). \
                values_list('institution', flat=True)
            departments = Department.objects.filter(
                institution_id__in=institution_ids)
            queryset = queryset.filter(department__in=departments)
        elif user.is_professor():
            queryset = queryset.filter(
                Q(state='posted', starts_at__lt=timezone.now()) |
                Q(committee=user.professor.id) |
                Q(electors=user.professor.id))
        if 'pk' in self.kwargs:
            return queryset.filter(id=self.kwargs['pk'])
        else:
            ids = queryset.values('code').annotate(Min('id')).values('id__min')
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


class RegistriesList(generics.ListAPIView):

    @detail_route()
    def members(self, request, pk=None):
        registry = self.get_object()
        members = registry.members
        ser = adapter.get_serializer('professors')
        return Response(
            ser(members, many=True, context={'request': request}).data)


USE_X_SEND_FILE = getattr(settings, 'USE_X_SEND_FILE', False)

class FilesViewSet(viewsets.ModelViewSet):

    @detail_route(methods=['get', 'head'])
    def download(self, request, pk=None):
        response = HttpResponse(content_type='applciation/force-download')
        user = request.user
        file = get_object_or_404(ApellaFile, id=pk)

        if request.method == 'HEAD':
            token = auth_hooks.generate_file_token(user, file)
            url = urlparse.urljoin(settings.BASE_URL, settings.API_PREFIX,
                                   reverse('apella-files-download', args=(pk,)))
            response['X-File-Location'] = "%s?token=%s" % (url, token)
            return response

        token = request.GET.get('token', None)
        if token is None:
            raise PermissionDenied("no.token")
            #url = reverse('apella-files-download', args=(pk,))
            #ui_url = getattr(settings, 'DOWNLOAD_FILE_URL', '')
            #ui_download_url = '%s?#download=%s' % (ui_url, url)
            #return HttpResponseRedirect(ui_download_url)

        token = request.GET.get('token', None)

        auth_hooks.consume_file_token(user, file, token)
        disp = 'attachment; filename=%s' % file.filename
        response['Content-Disposition'] = disp
        if USE_X_SEND_FILE:
            response['X-Sendfile'] = file.file_path.path
        else:
            response.content = open(file.file_path.path)
        return response

class UploadFilesViewSet(viewsets.ModelViewSet):

    FILE_SOURCE = {
        "Professor": "profile",
        "Candidate": "profile",
        "Candidacy": "candidacy",
        "Position": "position"
    }

    @detail_route(methods=['post'])
    def upload(self, request, pk=None):
        obj = self.get_object()
        if 'file_path' not in request.FILES:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        file_path = request.FILES['file_path']
        file_kind = request.data['file_kind']
        file_description = request.data['file_description']

        if file_kind not in FILE_KIND_TO_FIELD:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not file_path:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        field_name, many = FILE_KIND_TO_FIELD[file_kind].values()
        if field_name not in obj._meta.get_all_field_names():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = ApellaFile.objects.create(
                owner=request.user,
                file_kind=file_kind,
                source=self.FILE_SOURCE[obj.__class__.__name__],
                source_id=obj.id,
                file_path=file_path,
                description=file_description)

        if not many:
            setattr(obj, field_name, uploaded_file)
        else:
            many_attr = getattr(obj, field_name)
            many_attr.add(uploaded_file)
        obj.save()
        return Response(status=status.HTTP_200_OK)
