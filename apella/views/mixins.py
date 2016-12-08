from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import generics
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
        return InstitutionManager.objects.filter(manager_role='assistant')


class PositionList(generics.ListAPIView):
    """
        role institutionmanager: filter positions by institution/department
        role assistant: filter positions by author
    """
    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        if user.is_manager():
            im = InstitutionManager.objects.get(user_id=self.request.user.id)
            if user.is_institutionmanager():
                departments = Department.objects.filter(
                    institution_id=im.institution.id)
                queryset = queryset.filter(department__in=departments)
            elif user.is_assistant():
                queryset = queryset.filter(
                    author__user_id=self.request.user.id)
        if 'code' not in self.request.query_params:
            ids = queryset.values('code').annotate(Min('id')).values('id__min')
            return queryset.filter(id__in=ids)
        else:
            return queryset. \
                filter(code=self.request.query_params.get('code')). \
                order_by('created_at')
