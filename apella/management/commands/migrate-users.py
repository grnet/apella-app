import csv

from django.core.management import BaseCommand, CommandError

from apella.models import OldApellaUserMigrationData
from apella.migration_functions import migrate_username, migrate_shibboleth_id


class Command(BaseCommand):
    help = "Migrate users from csv"

    def add_arguments(self, parser):
        parser.add_argument('csv_file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        with open(csv_file_path) as f:
            csv_reader = csv.reader(f)

            csv_iterator = iter(csv_reader)
            for header in csv_iterator:
                break
            else:
                m = "No csv data"
                raise CommandError(m)

            for row in csv_iterator:
                old_user_id = row[0]
                old_users = OldApellaUserMigrationData.objects.filter(
                    user_id=old_user_id)
                if old_users[0].shibboleth_id:
                    migrate_shibboleth_id(
                        apella2_shibboleth_id=None,
                        old_apella_shibboleth_id=old_users[0].shibboleth_id)
                else:
                    migrate_username(old_users[0].username)
