from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from apella.models import SubjectArea, Subject


class Command(BaseCommand):
    help = 'Create a subject'
    args = '<title> <subject area id>'

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError("Invalid number of arguments")
        title, subject_area_id = args[:2]

        try:
            subject_area = SubjectArea.objects.get(id=subject_area_id)
            subject = Subject.objects.create(title=title, area=subject_area)
            self.stdout.write("Created subject %s : %s, area : %s" %
                    (subject.pk, subject.title, subject.area.title))
        except SubjectArea.DoesNotExist:
            raise CommandError("Subject area %s does not exist" %
                subject_area_id)
        except ValueError:
            raise CommandError(
                "Expected integer for <subject area id>, got: %s" %
                subject_area_id)
        except:
            raise
