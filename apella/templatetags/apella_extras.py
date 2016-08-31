from django import template
from apella.models import ApellaUser

register = template.Library()

@register.filter
def role(role_id):
    roles_dict = dict(ApellaUser.ROLES)
    return roles_dict[role_id] or ""
