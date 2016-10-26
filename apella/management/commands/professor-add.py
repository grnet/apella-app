from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from apella.models import ApellaUser, Professor, Institution, Department
from apella import common
from apella.management.utils import get_user, ApellaCommand


class Command(ApellaCommand):
    help = 'Create a professor from an existing user'

    def add_arguments(self, parser):
        parser.add_argument('user_id_or_username')
        parser.add_argument('institution_id')
        parser.add_argument('department_id')

    def handle(self, *args, **options):
        user_id_or_username = options['user_id_or_username']
        institution_id = options['institution_id']
        department_id = options['department_id']

        try:
            user = get_user(user_id_or_username)
            institution = Institution.objects.get(id=institution_id)
            department = Department.objects.get(id=department_id)
            a = Professor.objects.create(
                user=user, institution=institution, department=department)

            self.stdout.write("Professor with id: %s created" % a.pk)
        except ApellaUser.DoesNotExist:
            raise CommandError("User %s does not exist" % user_id_or_username)
        except Institution.DoesNotExist:
            raise CommandError(
                "Institution %s does not exist" % institution_id)
        except Department.DoesNotExist:
            raise CommandError("Department %s does not exist" % department_id)
