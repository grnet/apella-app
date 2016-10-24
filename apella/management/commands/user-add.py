from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from apella.management.utils import ApellaCommand
from apella.models import ApellaUser, ApellaUserEl, ApellaUserEn
from apella import common


class Command(ApellaCommand):
    help = 'Create a user'
    args = '<username> <password>'

    option_list = BaseCommand.option_list + (
        make_option('--role',
                    dest='role',
                    default=2,
                    choices=[x[0] for x in common.USER_ROLES],
                    help='Choose a role for the user'),
        )

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError("Invalid number of arguments")
        username, password = args[:2]

        try:
            el = ApellaUserEl.objects.create()
            en = ApellaUserEn.objects.create()

            a = ApellaUser.objects.create_user(
                    username=username,
                    password=password,
                    role=options['role'],
                    el=el,
                    en=en)

            self.stdout.write("User with id: %s created" % a.pk)
        except:
            raise
