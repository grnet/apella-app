from django.core.management import BaseCommand

from apella.models import Position, Department


class Command(BaseCommand):
    help = "Fix migrated positions dep number"

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', dest='dry_run')

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        empty_positions = Position.objects.filter(department_dep_number=0)
        for p in empty_positions:
            dep_number = p.department.dep_number
            if dep_number is not None:
                if dry_run:
                    self.stdout.write(
                        'will set position\'s %r dep number to %r' %
                        (p.id, dep_number))
                else:
                    p.department_dep_number = dep_number
                    p.save()
                    self.stdout.write(
                        'updated position\'s %r dep number: %r' %
                        (p.id, dep_number))
