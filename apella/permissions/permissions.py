from urlparse import urlparse

from django.conf import settings
from django.apps import apps
from rest_framework.permissions import BasePermission

from apella.permissions.permission_rules import tb


def get_resource(url):

    parsed = urlparse(url)
    segments = parsed.path.strip('/').split('/')

    if segments[-1].isdigit():
        resource = str(segments[-2])
        resource_id = segments[-1]
    else:
        resource = str(segments[-1])
        resource_id = None

    return resource, resource_id


def get_context_from_request(request, view):
    role = request.user.role
    resource, resource_id = get_resource(request.path)
    action = str(view.action)

    model_name = settings.API_SCHEMA_TMP['resources'][resource]['model']
    parts = model_name.split('.')
    model_name = parts[-1]
    model = apps.get_model(app_label='apella', model_name=model_name)
    pattern_row = tb.Row(
            role=role, resource=resource, field='*',
            action=action, state='*', section='*')

    return role, action, resource, resource_id, model, pattern_row


def check_state_conditions(
        matches, request, view, model, obj=None, is_collection=True):

    for row in matches:
        if row.state == '*':
            return True
        prefix = 'check_collection_state_' \
            if is_collection else 'check_object_state_'
        check_name = prefix + row.state
        check_method = getattr(model, check_name, None)
        if callable(check_method):
            if is_collection:
                ret = check_method(row=row, request=request, view=view)
            else:
                ret = check_method(obj, row=row, request=request, view=view)
            if ret:
                return True
    return False


class PermissionRulesCheck(BasePermission):

    def has_permission(self, request, view):

        role, action, resource, resource_id, model, pattern_row = \
                get_context_from_request(request, view)
        if action == 'partial_update':
            matches = tb.match(pattern_row, expand={'field'})
            allowed_keys = {x.field for x in matches}
            if '*' in allowed_keys:
                return True
            fields_to_update = set(request.data.keys())
            if fields_to_update - allowed_keys:
                return False
        if not resource_id:
            matches = tb.match(pattern_row, expand={'state'})
            return check_state_conditions(matches, request, view, model)
        return True

    def has_object_permission(self, request, view, obj):

        role, action, resource, resource_id, model, pattern_row =\
                get_context_from_request(request, view)
        matches = tb.match(pattern_row, expand={'state', 'field'})
        return check_state_conditions(
            matches, request, view, model, obj, False)
