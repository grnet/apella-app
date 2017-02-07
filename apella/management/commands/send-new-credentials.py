from apella.management.utils import ApellaCommand
from apella.models import OldApellaUserMigrationData as OldUsers, ApellaUser
from apella.emails import send_new_credentials_to_old_users_email


class Command(ApellaCommand):
    help = 'Send new credentials email to old apella users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            dest='dry_run',
            help='List users that will receive email'
        )
        parser.add_argument(
            '--institution',
            dest='institution',
            help='Select specified institution\'s users to receive email'
        )

    def handle(self, *args, **options):
        institution = options['institution']
        emails = OldUsers.objects. \
            exclude(permanent_auth_token__isnull=True). \
            exclude(permanent_auth_token__exact=''). \
            filter(role_status='ACTIVE', shibboleth_id='', passwd=''). \
            values_list('email', flat=True).distinct()

        if institution:
            emails = emails.filter(professor_institution_id=institution)

        dry_run = options['dry_run']
        for email in emails:
            if ApellaUser.objects.filter(email=email).exists():
                self.stdout.write(
                    'ApellaUser with email %s already exists.' % email)
                continue
            if dry_run:
                self.stdout.write('%s' % email)
            else:
                old_users = OldUsers.objects.filter(email__iexact=email)
                send_new_credentials_to_old_users_email([old_users[0]])
                self.stdout.write('new credentials email sent to %s' % email)
