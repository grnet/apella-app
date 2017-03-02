from django.core.management import BaseCommand

from apella.models import Candidacy, OldApellaCandidacyMigrationData

class Command(BaseCommand):
    help = "Fix cancelled migrated candidacies"

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', dest='dry_run')

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        cancelled = Candidacy.objects.filter(state='cancelled')
        for c in cancelled:
            if c.old_candidacy_id:
                try:
                    old = OldApellaCandidacyMigrationData.objects.get(
                        candidacy_serial=c.old_candidacy_id)
                except OldApellaCandidacyMigrationData.DoesNotExist:
                    self.stdout.write('failed to find old %r', c.old_candidacy_id)
                    continue

                if not old.withdrawn_at:
                    if not dry_run:
                        c.state = 'posted'
                        c.save()
                        self.stdout.write(
                            'fixed cancelled candidacy %s, old %s' %
                            (c.id, old.candidacy_serial))
                    else:
                        self.stdout.write(
                            'new %s, old %s' % (str(c.id), old.candidacy_serial))
