from rest_framework.permissions import BasePermission


class TermsPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'accept_terms':
            return True
        user = request.user
        if not hasattr(user, 'has_accepted_terms'):
            return True
        else:
            return request.user.has_accepted_terms
