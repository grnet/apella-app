from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from apella.models import ApellaUser


class Command(BaseCommand):
    help = 'Create a user'
    args = '<username password>'

    option_list = BaseCommand.option_list + (
        make_option('--role',
                    dest='role',
                    default=2,
                    choices=[x[0] for x in ApellaUser.ROLES],
                    help='Choose a role for the user'),
        )

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError("Invalid number of arguments")
        username, password = args[:2]

        try:
            a = ApellaUser.objects.create(username=username,
                                          password=password,
                                          role=options['role'])

            self.stdout.write("User with id: %s created" % a.pk)
        except BaseException, e:
            raise CommandError(e)
        except:
            self.stdout.write("Operation failed")
