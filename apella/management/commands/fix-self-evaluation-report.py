import logging

from django.core.management import BaseCommand

from apella.models import Candidacy, OldApellaCandidacyFileMigrationData
from apella.migration_functions import migrate_file

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Migrate missing self evaluation report files from candidacies"

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', dest='dry_run')

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        candidacies = Candidacy.objects.exclude(old_candidacy_id=None). \
            filter(self_evaluation_report=None).order_by('-updated_at')
        for c in candidacies:
            old_reports = OldApellaCandidacyFileMigrationData.objects.filter(
                candidacy_serial=c.old_candidacy_id,
                candidate_user_id=str(c.candidate.old_user_id),
                file_type='EKTHESI_AUTOAKSIOLOGISIS')
            if len(old_reports) == 0:
                logger.info(
                    'self evaluation report not found '
                    'for old candidacy %r', c.old_candidacy_id)
                continue
            old_report = old_reports[0]
            if not dry_run:
                migrate_file(old_report, c.candidate, 'candidacy', c.id)
                logger.info(
                    'migrated old file %s to candidacy %r' %
                    (old_report.file_id, c.id))
            else:
                logger.info(
                    'will migrate old file %s to candidacy %r' %
                    (old_report.file_id, c.id))
