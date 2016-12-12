from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from apella.management.utils import ApellaCommand
from apella.models import Department


class Command(ApellaCommand):
    help = 'Modify department'
    args = '<department id>'

    option_list = BaseCommand.option_list + (
        make_option('--dep_number',
                    dest='dep_number',
                    help='Department\'s DEP number'),
        )

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Invalid number of arguments")
        department_id = args[0]
        dep_number = options['dep_number']

        try:
            department = Department.objects.get(id=department_id)
            department.dep_number = dep_number
            department.save()
            self.stdout.write(
                "Modified department %s" % department.pk)
        except Department.DoesNotExist:
            raise CommandError('Department %s does not exist' % department_id)
        except ValueError:
            raise CommandError('Department\'s DEP number must be an insteger')
