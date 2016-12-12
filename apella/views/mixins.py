from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import detail_route
from django.db.models import ProtectedError, Min

from apella.models import InstitutionManager, Position, Department


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


class PositionList(generics.ListAPIView):

    @detail_route()
    def history(self, request, pk=None):
        position = self.get_object()
        user = self.request.user
        position_states = Position.objects.filter(code=position.code)
        serializer = self.get_serializer(position_states, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if user.is_manager():
            institution_ids = InstitutionManager.objects.filter(user=user). \
                values_list('institution', flat=True)
            if user.is_institutionmanager():
                departments = Department.objects.filter(
                    institution_id__in=institution_ids)
                queryset = queryset.filter(department__in=departments)
            elif user.is_assistant():
                queryset = queryset.filter(author__user_id=user.id)
        ids = queryset.values('code').annotate(Min('id')).values('id__min')
        return queryset.filter(id__in=ids)


class CandidacyList(generics.ListAPIView):

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
        return queryset
