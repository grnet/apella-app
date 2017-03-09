from django.core.management import BaseCommand, CommandError

from apella.installation_validations import remove_unreferenced_apella_files
from apella.models import ApellaFile, ApellaUser

import sys
import logging
logger = logging.getLogger()


class Command(BaseCommand):
    help = "Remove unreferenced ApellaFile instances from database"

    def add_arguments(self, parser):
        parser.add_argument(
            '--usernames',
            dest='usernames',
            default=False,
            nargs='?',
            help=('","-separated username list. '
                  'Leave empty for a list of all usernames. '
                  'Use - to read one per line from standard input.'),
        )

        parser.add_argument(
            '--force',
            action='store_true',
            help="Force removal. Do not pretend. No dry run.",
        )

    def handle(self, *args, **options):
        force = options.get('force', False)
        usernames = options.get('usernames', False)
        if usernames is False:
            files = ApellaFile.objects.all()

        elif not usernames:
            usernames = ApellaUser.objects.all()
            usernames = usernames.values_list('username', flat=True)
            usernames = usernames.order_by('username')
            for username in usernames:
                self.stdout.write(username + '\n')
            raise SystemExit

        else:
            if usernames == '-':
                userlist = [x.strip() for x in sys.stdin]
            else:
                userlist = usernames.split(',')

            files = ApellaFile.objects.filter(owner__username__in=userlist)

        logger.info("Checking %d files" % files.count())

        remove_unreferenced_apella_files(files=files, force=force)
