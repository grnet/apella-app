#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import logging
import re

from django.core.management.base import CommandError

from rest_framework import serializers

from apella.models import ApellaUser
from apella.management.utils import ApellaCommand
from apella.serializers.position import upgrade_candidate_to_professor

logger = logging.getLogger(__name__)

RANKS = {
    'ΕΠΙΚΟΥΡΟΣ ΚΑΘΗΓΗΤΗΣ': 'Assistant Professor',
    'ΛΕΚΤΟΡΑΣ': 'Lecturer',
    'ΕΠΙ ΘΗΤΕΙΑ ΕΠΙΚΟΥΡΟΣ ΚΑΘΗΓΗΤΗΣ': 'Tenured Assistant Professor',
    'ΑΝΑΠΛΗΡΩΤΗΣ ΚΑΘΗΓΗΤΗΣ': 'Associate Professor',
    'ΚΑΘΗΓΗΤΗΣ': 'Professor',
    'ΚΥΡΙΟΣ ΕΡΕΥΝΗΤΗΣ': 'Principal Researcher',
    'ΕΝΤΕΤΑΛΜΕΝΟΣ ΕΡΕΥΝΗΤΗΣ': 'Affiliated Researcher',
    'ΔΙΕΥΘΥΝΤΗΣ ΕΡΕΥΝΩΝ': 'Principal Researcher'
}


class Command(ApellaCommand):
    help = 'Create or update a registry of the given type'

    def add_arguments(self, parser):
        parser.add_argument('csv_file')
        parser.add_argument('--dry-run',
                            dest='dry_run')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        dry_run = options['dry_run']

        with open(csv_file_path) as f:
            csv_reader = csv.reader(f)

            csv_iterator = iter(csv_reader)
            for header in csv_iterator:
                break
            else:
                raise CommandError("No csv data")

            for user_id, last_name, first_name, father_name, department_id, \
                    email, rank, fek, fek_subject, subject_in_fek \
                    in csv_iterator:
                try:
                    user = ApellaUser.objects.get(id=user_id)
                except ApellaUser.DoesNotExist:
                    logger.error(
                        "User with id %r does not exist" % user_id)
                    continue

                rank = [v for k, v in RANKS.items() if k == rank]
                if not dry_run:
                    try:
                        upgrade_candidate_to_professor(
                                user,
                                department=department_id,
                                rank=rank[0],
                                fek=fek,
                                discipline_text=fek_subject,
                                discipline_in_fek=bool(
                                    re.match('true', subject_in_fek, re.I)))
                    except serializers.ValidationError as ve:
                        logger.error(
                            "failed to upgrade user %r: %s" % (user_id, ve))
                else:
                    logger.info(
                        'will upgrade user %r to professor' % user_id)
