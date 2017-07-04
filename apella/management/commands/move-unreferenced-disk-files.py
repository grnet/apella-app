import os
from django.core.management import BaseCommand, CommandError

from apella.installation_validations import move_unreferenced_disk_files


class Command(BaseCommand):
    help = "Move disk files that are not referenced by db into destination"

    def add_arguments(self, parser):
        parser.add_argument(
            'dest',
            help=('Destination directory to move files into. '
                  'Should be in the same file system.')
        )

        parser.add_argument(
            '--force',
            action='store_true',
            help='Force move. Do not pretend. No dry run.',
        )

    def handle(self, *args, **options):
        dest = options.get('dest')
        force = options.get('force', False)

        if not dest:
            raise CommandError("No destination given.")

        dest = os.path.realpath(dest)
        if not os.path.isdir(dest):
            os.makedirs(dest)

        move_unreferenced_disk_files(dest, force=force)
