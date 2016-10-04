from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from apella.management.utils import ApellaCommand
from apella.models import Department, School


class Command(ApellaCommand):
    help = 'Create a department for the given school'
    args = '<school id> <title>'

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError("Invalid number of arguments")
        school_id, title = args[:2]

        try:
            school = School.objects.get(id=school_id)
            department = Department.objects.create(
                school=school, title=title)
            self.stdout.write(
                "Created department %s : %s" %
                (department.pk, department.title))
        except School.DoesNotExist:
            raise CommandError("School %s does not exist" % school_id)
        except BaseException, e:
            raise CommandError(e)
