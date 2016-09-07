from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from apella.models import Institution


class Command(BaseCommand):
    help = 'Create an institution'
    args = '<title>'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Invalid number of arguments")
        title = args[0]

        try:
            institution = Institution.objects.create(title=title)
            self.stdout.write("Created institution %s : %s" %
                    (institution.pk, institution.title))
        except BaseException, e:
            raise CommandError(e)
        except:
            self.stdout.write("Operation failed")
