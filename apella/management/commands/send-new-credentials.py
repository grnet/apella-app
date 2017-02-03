from apella.management.utils import ApellaCommand
from apella.models import OldApellaUserMigrationData as OldUsers
from apella.emails import send_new_credentials_to_old_users_email


class Command(ApellaCommand):
    help = 'Send new credentials email to old apella users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            dest='dry_run',
            help='List users that will receive email'
        )

    def handle(self, *args, **options):
        emails = OldUsers.objects. \
            exclude(permanent_auth_token__isnull=True). \
            exclude(permanent_auth_token__exact=''). \
            filter(role_status='ACTIVE', shibboleth_id='', passwd=''). \
            values_list('email', flat=True).distinct()

        dry_run = options['dry_run']
        for email in emails:
            if dry_run:
                self.stdout.write('%s' % email)
            else:
                old_users = OldUsers.objects.filter(email__iexact=email)
                send_new_credentials_to_old_users_email([old_users[0]])
                self.stdout.write('new credentials email sent to %s' % email)

        self.stdout.write('Found %d emails' % emails.count())
