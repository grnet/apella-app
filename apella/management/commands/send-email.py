from django.core.management.base import CommandError

from apella.management.utils import ApellaCommand
from apella.models import OldApellaUserMigrationData as OldUsers, ApellaUser
from apella.emails import send_user_email


class Command(ApellaCommand):
    help = 'Send specified email template to apella users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--template-body',
            dest='template_body',
            help='Email body template'
        )
        parser.add_argument(
            '--template-subject',
            dest='template_subject',
            help='Email subject template'
        )
        parser.add_argument(
            '--shibboleth',
            dest='shibboleth',
            help='Select shibboleth users'
        )
        parser.add_argument(
            '--foreign',
            dest='foreign',
            help='Select foreign professors'
        )
        parser.add_argument(
            '--candidate',
            dest='candidate',
            help='Select candidates'
        )
        parser.add_argument(
            '--list',
            dest='list',
            help='List emails'
        )

    def handle(self, *args, **options):
        template_body = options['template_body']
        shibboleth = options['shibboleth']
        candidate = options['candidate']
        foreign = options['foreign']
        subject = options['template_subject']
        list_emails = options['list']

        if not subject:
            raise CommandError('no subject')

        if not template_body:
            raise CommandError('no body')

        emails = []
        if shibboleth:
            emails = OldUsers.objects. \
                filter(role_status='ACTIVE'). \
                exclude(shibboleth_id=''). \
                values_list('email', flat=True).distinct()
        elif foreign:
            emails = OldUsers.objects. \
                filter(role_status='ACTIVE', is_foreign='t'). \
                values_list('email', flat=True).distinct()
        elif candidate:
            candidates = OldUsers.objects.filter(
                role_status='ACTIVE', shibboleth_id='',
                permanent_auth_token='', role='candidate')
            for c in candidates:
                if not OldUsers.objects.filter(
                    email=c.email, role='professor').exists():
                        emails.append(c.email)



        for email in emails:
            if list_emails:
                self.stdout.write(email)
            else:
                old_users = OldUsers.objects.filter(email__iexact=email)
                send_user_email(
                    old_users[0],
                    subject,
                    template_body
                    )
                self.stdout.write('email sent to %s' % email)
