from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import generics
from django.db.models import ProtectedError

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
        if InstitutionManager.objects.filter(
                user_id=self.request.user.id).exists():
            im = InstitutionManager.objects.get(user_id=self.request.user.id)
            if im.user.role == 'institutionmanager':
                departments = Department.objects.filter(
                    institution_id=im.institution.id)
                return Position.objects.filter(
                    department__in=departments)
            elif im.user.role == 'assistant':
                return Position.objects.filter(
                    author__user_id=im.user.id)
        return super(PositionList, self).get_queryset()
