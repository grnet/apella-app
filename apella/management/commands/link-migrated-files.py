import csv

from django.core.management import BaseCommand, CommandError

from apella.migration_functions import link_migrated_files
from apella.models import ApellaFile


class Command(BaseCommand):
    help = "Ensure migrated files are hard-linked on disk"

    def handle(self, *args, **options):
        files = ApellaFile.objects.exclude(old_file_path='')
        link_migrated_files(files)
