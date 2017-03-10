import os

from django.conf import settings

from apella.management.utils import ApellaCommand
from apella.models import Professor
from apella.emails import send_user_email_attachment


class Command(ApellaCommand):
    help = 'Send evaluators announcement to professors'

    def add_arguments(self, parser):
        parser.add_argument(
            '--attachment',
            dest='attachment',
            help='Path to file attachment'
        )
        parser.add_argument(
            '--dry-run',
            dest='dry_run',
            help='Dry run'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        attachment = options['attachment']

        if not attachment:
            attachment = os.path.join(
                settings.RESOURCES_DIR, 'attachment.pdf')
        subject = 'apella/emails/evaluators_subject.txt'
        body = 'apella/emails/evaluators_body.txt'

        professors = Professor.objects.filter(
            is_foreign=False, user__is_active=True, is_verified=True)
        for p in professors:
            if not dry_run:
                send_user_email_attachment(
                    p.user, subject, body, attachment)
            else:
                self.stdout.write(p.user.email)
