#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

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

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        attachment1 = os.path.join(
            settings.RESOURCES_DIR, 'attachment1.pdf')
        attachment2 = os.path.join(
            settings.RESOURCES_DIR, 'attachment2.pdf')
        template_subject = 'apella/emails/evaluators_subject.txt'
        subject = render_to_string(template_subject).replace('\n', ' ')
        template_body = 'apella/emails/evaluators_body.txt'
        body = render_to_string(template_body)

        professors = Professor.objects.filter(
            is_foreign=False, user__is_active=True, is_verified=True)
        for p in professors:
            if not dry_run:
                message = EmailMessage(
                    subject, body, settings.DEFAULT_FROM_EMAIL, [p.user.email])
                message.attach(
                    'ΠΡΟΣΚΛΗΣΗ ΓΙΑ ΕΓΓΡΑΦΗ ΣΤΟ ΜΗΤΡΩΟ ΑΞΙΟΛΟΓΗΤΩΝ'.decode('utf-8'),
                    attachment1,
                    'application/pdf')
                message.attach(
                    'ΜΕΘΟΛΟΓΙΑ ΑΞΙΟΛΟΓΗΣΗΣ ΕΔΒΜ 34'.decode('utf-8'),
                    attachment2,
                    'application/pdf')
                message.send()
                self.stdout.write('email sent to %s' % p.user.email)
            else:
                self.stdout.write(p.user.email)
