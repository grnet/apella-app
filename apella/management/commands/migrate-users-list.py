import csv

from django.core.management import BaseCommand

from apella.models import OldApellaUserMigrationData


class Command(BaseCommand):
    help = "List users to be migrated"

    def handle(self, *args, **options):
        old_users = OldApellaUserMigrationData.objects. \
            exclude(email='').exclude(role='assistant'). \
            values_list('username', 'shibboleth_id').distinct()

        fields = ['username', 'shibboleth_id']
        with open('migrate_users_list.csv', 'wb') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
            for user in old_users:
                writer.writerow(user)
