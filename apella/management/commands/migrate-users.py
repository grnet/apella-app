import logging
logger = logging.getLogger('apella')

import csv

from django.core.management import BaseCommand, CommandError

from apella.models import OldApellaUserMigrationData
from apella.migration_functions import migrate_username, migrate_shibboleth_id


class Command(BaseCommand):
    help = "Migrate users from csv"

    def add_arguments(self, parser):
        parser.add_argument('csv_file')
        parser.add_argument('-p', '--parallel',
                            dest='parallel', type=str, default='1/1',
                            help="Execute (part of) user migrations. Default: 1/1")

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        parallel = options['parallel']
        import re
        parallel_pattern = '^[1-9][0-9]*/[1-9][0-9]*$'
        if not re.match(parallel_pattern, parallel):
            m = "Parallel specification must be in the form %r, not %r"
            m %= (parallel_pattern, parallel)
            raise CommandError(m)

        this_part_no, nr_all_parts = parallel.split('/')
        this_part_no = int(this_part_no)
        nr_all_parts = int(nr_all_parts)
        if this_part_no > nr_all_parts:
            m = ("This part number %d cannot be greater "
                 "than the number of all parts %d")
            m %= (this_part_no, nr_all_parts)
            raise CommandError(m)

        with open(csv_file_path) as f:
            csv_reader = csv.reader(f)
            csv_iterator = iter(csv_reader)
            for header in csv_iterator:
                break
            else:
                m = "No csv data"
                raise CommandError(m)

            nr_lines = 0
            for row in csv_iterator:
                nr_lines += 1
        
        part_size = nr_lines / nr_all_parts
        start_line_no = part_size * (this_part_no - 1)
        end_line_no = nr_lines \
            if this_part_no == nr_all_parts \
            else (start_line_no + part_size)

        with open(csv_file_path) as f:
            csv_reader = csv.reader(f)

            csv_iterator = iter(csv_reader)
            for header in csv_iterator:
                break
            else:
                m = "No csv data"
                raise CommandError(m)

            line_no = 0
            for username, shibboleth_id in csv_iterator:
                if start_line_no <= line_no < end_line_no:
                    if line_no % 100 == 0:
                        m = "migrating %d <= %d < %d"
                        m %= (start_line_no, line_no, end_line_no)
                        logger.info(m)
                    if shibboleth_id:
                        migrate_shibboleth_id(
                            apella2_shibboleth_id=None,
                            old_apella_shibboleth_id=shibboleth_id)
                    else:
                        migrate_username(username)
                line_no += 1
