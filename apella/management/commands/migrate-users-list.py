import csv

from django.core.management import BaseCommand, CommandError

from apella.models import OldApellaUserMigrationData


class Command(BaseCommand):
    help = "List users to be migrated"

    def handle(self, *args, **options):
        password_users = OldApellaUserMigrationData.objects.filter(
            shibboleth_id='').exclude(email='').exclude(role='assistant')
        shibboleth_users = OldApellaUserMigrationData.objects.exclude(
            shibboleth_id='').exclude(email='')

        fields = [
            'user_id', 'username', 'shibboleth_id',
            'role', 'name_el', 'surname_el', 'role_status'
        ]
        with open('migrate_users_list.csv', 'wb') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
            for user in password_users | shibboleth_users:
                writer.writerow(
                    [unicode(getattr(user, field)).encode('utf-8')
                     for field in fields])
