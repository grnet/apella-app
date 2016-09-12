from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from apella.models import SubjectArea


class Command(BaseCommand):
    help = 'Create a subject area'
    args = '<title>'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Invalid number of arguments")
        title = args[0]

        try:
            subject_area = SubjectArea.objects.create(title=title)
            self.stdout.write("Created subject area %s : %s" %
                    (subject_area.pk, subject_area.title))
        except BaseException, e:
            raise CommandError(e)
        except:
            self.stdout.write("Operation failed")
