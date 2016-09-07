from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from apella.models import Department, Institution


class Command(BaseCommand):
    help = 'Create a department'
    args = '<institution id> <title>'

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError("Invalid number of arguments")
        institution_id, title = args[:2]

        try:
            institution = Institution.objects.get(id=institution_id)
            department = Department.objects.create(
                    institution=institution,title=title)
            self.stdout.write("Created department %s : %s" %
                    (department.pk, department.title))
        except Institution.DoesNotExist:
            raise CommandError("Institution %s does not exist" % institution_id)
        except BaseException, e:
            raise CommandError(e)
