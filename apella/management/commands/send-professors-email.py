#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from email.header import Header

from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from apella.management.utils import ApellaCommand
from apella.models import Professor


class Command(ApellaCommand):
    help = 'Send evaluators announcement to professors'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            dest='dry_run',
            help='Dry run'
        )
        parser.add_argument(
            '--test-email',
            dest='test_email',
            help='Email address to test'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        test_email = options['test_email']

        attachment1 = os.path.join(
            settings.RESOURCES_DIR, 'attachment1.pdf')
        with open(attachment1, 'r') as f1:
            content1 = f1.read()
        attachment2 = os.path.join(
            settings.RESOURCES_DIR, 'attachment2.pdf')
        with open(attachment2, 'r') as f2:
            content2 = f2.read()

        template_subject = 'apella/emails/evaluators_subject.txt'
        subject = render_to_string(template_subject).replace('\n', ' ')
        template_body = 'apella/emails/evaluators_body.txt'
        body = render_to_string(template_body)

        if not test_email:
            professors = Professor.objects.filter(
                is_foreign=False, user__is_active=True, is_verified=True)
            for p in professors:
                if not dry_run:
                    message = EmailMessage(
                        subject, body, settings.DEFAULT_FROM_EMAIL, [p.user.email])
                    message.attach(
                        Header(
                            u'ΠΡΟΣΚΛΗΣΗ ΓΙΑ ΕΓΓΡΑΦΗ ΣΤΟ ΜΗΤΡΩΟ ΑΞΙΟΛΟΓΗΤΩΝ.pdf',
                            'utf-8').encode(),
                        content1,
                        'application/pdf')
                    message.attach(
                        Header(
                            u'ΜΕΘΟΛΟΓΙΑ ΑΞΙΟΛΟΓΗΣΗΣ ΕΔΒΜ 34.pdf',
                            'utf-8').encode(),
                        content2,
                        'application/pdf')
                    message.send()
                    self.stdout.write('email sent to %s' % p.user.email)
                else:
                    self.stdout.write(p.user.email)
        else:
            message = EmailMessage(
                subject, body, settings.DEFAULT_FROM_EMAIL, [test_email])
            message.attach(
                Header(
                    u'ΠΡΟΣΚΛΗΣΗ ΓΙΑ ΕΓΓΡΑΦΗ ΣΤΟ ΜΗΤΡΩΟ ΑΞΙΟΛΟΓΗΤΩΝ',
                    'utf-8').encode(),
                content1,
                'application/pdf')
            message.attach(
                Header(
                    u'ΜΕΘΟΛΟΓΙΑ ΑΞΙΟΛΟΓΗΣΗΣ ΕΔΒΜ 34',
                    'utf-8').encode(),
                content2,
                'application/pdf')
            message.send()
