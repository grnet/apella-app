from apella.models import ApellaUser


def get_user(identifier, **kwargs):
    try:
        if identifier.isdigit():
            return ApellaUser.objects.get(id=int(identifier))
        else:
            return ApellaUser.objects.get(username__iexact=identifier)
    except (ApellaUser.DoesNotExist):
        raise
