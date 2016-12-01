from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import generics
from django.db.models import ProtectedError

from apella.models import InstitutionManager


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
