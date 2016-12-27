from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import detail_route
from django.db.models import ProtectedError, Min, Q
from django.conf import settings
from django.utils import timezone

from apimas.modeling.adapters.drf.mixins import HookMixin

from apella.models import InstitutionManager, Position, Department, \
        Candidacy, ApellaUser, ApellaFile, ElectorParticipation
from apella.loader import adapter


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
        if user.is_institutionmanager():
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


class PositionList(object):

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

    def update(self, request, pk=None):
        position = self.get_object()
        code = position.code
        if code.split(settings.POSITION_CODE_PREFIX)[1] != \
                str(position.id):
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super(PositionList, self).update(request, pk=None)


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


class DepartmentList(generics.ListAPIView):

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if isinstance(user, ApellaUser):
            if user.is_manager():
                institution_ids = InstitutionManager.objects. \
                    filter(user=user).values_list('institution', flat=True)
                queryset = queryset.filter(institution_id__in=institution_ids)
        return queryset


class RegistriesList(generics.ListAPIView):

    @detail_route()
    def members(self, request, pk=None):
        registry = self.get_object()
        members = registry.members
        ser = adapter.get_serializer('professors')
        return Response(
            ser(members, many=True, context={'request': request}).data)


class UploadFilesViewSet(viewsets.ModelViewSet):

    FILE_SOURCE = {
        "Professors": "profile",
        "Candidates": "profile",
        "Candidacies": "candidacy",
        "Positions": "position"
    }

    @detail_route(methods=['put'])
    def upload(self, request, pk=None):
        candidate = self.get_object()
        cv = ApellaFile.objects.create(
            owner=request.user,
            file_kind='CV',
            source=self.FILE_SOURCE[self.get_view_name()],
            source_id=candidate.id,
            file_path=request.FILES['cv.file_path'])
        candidate.cv = cv
        candidate.save()
        return Response(status=status.HTTP_200_OK)
