from django.core.management.base import CommandError
from apella.management.utils import ApellaCommand
from apella.models import ApellaUser
from apella import common


class Command(ApellaCommand):
    help = 'List users'

    def handle(self, *args, **options):
        if args:
            raise CommandError("Command does not accept any arguments")

        try:
            users = ApellaUser.objects.all()
            roles_dict = dict(common.USER_ROLES)
            if users:
                self.stdout.write('ID\tUsername\tRole_ID\t Role')
            for user in users:

                role = roles_dict[user.role]
                self.stdout.write('%s\t%s\t\t%s\t%s' % (
                    user.id, user.username, user.role, role))
        except:
            raise
