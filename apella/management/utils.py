import locale

from django.utils.encoding import smart_unicode
from django.core.management import BaseCommand
from django.conf import settings
from django.apps import apps

from apella.models import ApellaUser


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
    encoding = locale.getpreferredencoding() or 'utf8'
    return smart_unicode(s, encoding=encoding, **kwargs)


class ApellaCommand(BaseCommand):

    def run_from_argv(self, argv):
        argv = [smart_locale_unicode(a) for a in argv]
        super(ApellaCommand, self).run_from_argv(argv)


class LoadDataCommand(BaseCommand):

    MODEL = None

    help = "Loads data from a .csv file"

    def add_arguments(self, parser):
        parser.add_argument('csv_file')

    def preprocess(self, input_line):
        return input_line.strip().strip(';').split(';')
