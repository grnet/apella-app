from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from apella.models import InstitutionManager, Institution, ApellaUser
from apella import common
from apella.management.utils import get_user, ApellaCommand


class Command(ApellaCommand):
    help = 'Create an institution manager'
    args = '<user id or username> <institution id>'

    option_list = BaseCommand.option_list + (
        make_option('--role',
                    dest='role',
                    default='manager',
                    choices=[x[0] for x in common.MANAGER_ROLES],
                    help='Choose a role for the user'),
        )

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError("Invalid number of arguments")
        user_id_or_username, institution_id = args[:2]

        try:
            user = get_user(user_id_or_username)
            institution = Institution.objects.get(id=institution_id)
            a = InstitutionManager.objects.create(
                user=user,
                institution=institution,
                manager_role=options['role'])

            self.stdout.write("InstitutionManager with id: %s created" % a.pk)
        except ApellaUser.DoesNotExist:
            raise CommandError("User %s does not exist" % user_id_or_username)
        except Institution.DoesNotExist:
            raise CommandError(
                "Institution %s does not exist" % institution_id)
