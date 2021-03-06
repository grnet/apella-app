from django.core.management import BaseCommand, CommandError
from django.db import transaction
import apella.models
import csv
import os
import sys
from datetime import datetime


def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Command(BaseCommand):

    help = (
        "Load migration data from a .csv file into a target model.\n"
        "Model name defaults to the name of the csv file.\n"
    )

    def add_arguments(self, parser):
        parser.add_argument('-m', '--model-name', dest='model_name')
        parser.add_argument('csv_file')

    def preprocess(self, input_line):
        return input_line.strip().strip(';').split(';')

    @transaction.atomic
    def read_csv_file(self, csv_reader, target_model_name):
        modelclass = getattr(apella.models, target_model_name, None)
        if modelclass is None:
            m = "model not found: {0!r}".format(target_model_name)
            raise CommandError(m)

        count = modelclass.objects.all().count()
        if count:
            m = "Delete {0!r} existing rows in model {1!r} (y/n)? "
            m = m.format(count, target_model_name)
            sys.stdout.write(m)
            sys.stdout.flush()
            line = sys.stdin.readline()

            if line.strip().lower() != 'y':
                m = "Not confirmed."
                raise RuntimeError(m)

            modelclass.objects.all().delete()

        csv_iterator = iter(csv_reader)
        for header in csv_iterator:
            break
        else:
            m = "No csv data"
            raise CommandError(m)

        counter = 0

        field_names = tuple(str(x) for x in header)
        for row in csv_iterator:

            modelinstance = modelclass()

            for name, value in zip(field_names, row):
                setattr(modelinstance, name, value)
            modelinstance.save()
            counter += 1
            if counter % 100 == 0:
                m = "{0}: Imported {1!r} rows so far.".format(now(), counter)
                self.stdout.write(m)

        m = "{0}: Imported a total of {1!r} rows.".format(now(), counter)
        self.stdout.write(m)

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        target_model_name = options.get('model_name')
        if not target_model_name:
            target_model_name = os.path.basename(csv_file_path)
            target_model_name = target_model_name.rsplit(os.path.extsep)[0]

        with open(csv_file_path) as f:
            csv_reader = csv.reader(f)
            self.read_csv_file(csv_reader, target_model_name)
