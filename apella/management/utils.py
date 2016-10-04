from apella.models import ApellaUser
from django.utils.encoding import smart_unicode
from django.core.management import BaseCommand
from django.utils.encoding import smart_unicode
import locale


def get_user(identifier, **kwargs):
    try:
        if identifier.isdigit():
            return ApellaUser.objects.get(id=int(identifier))
        else:
            return ApellaUser.objects.get(username__iexact=identifier)
    except (ApellaUser.DoesNotExist):
        raise


def smart_locale_unicode(s, **kwargs):
    """Wrapper around 'smart_unicode' using user's preferred encoding."""
    encoding = locale.getpreferredencoding()
    return smart_unicode(s, encoding=encoding, **kwargs)


class ApellaCommand(BaseCommand):

    def run_from_argv(self, argv):
        argv = [smart_locale_unicode(a) for a in argv]
        super(ApellaCommand, self).run_from_argv(argv)
