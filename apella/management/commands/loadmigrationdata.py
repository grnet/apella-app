from django.core.management import BaseCommand, CommandError
import apella.models
import csv


class Command(BaseCommand):

    help = "Load migration data from a .csv file into a target model."

    def add_arguments(self, parser):
        parser.add_argument('target_model_name')
        parser.add_argument('csv_file')

    def preprocess(self, input_line):
        return input_line.strip().strip(';').split(';')


    def read_csv_file(csv_reader, target_model_name):
        modelclass = getattr(apella.models, target_model_name, None)
        if modelclass is None:
            m = "model not found: {0!r}".format(target_model_name)
            raise CommandError(m)

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

        self.stdout.write("Imported {0!r} rows.".format(counter))

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        target_model_name = options['target_model_name']
        with open(csv_file_path) as f:
            csv_reader = csv.reader(f)
            self.read_csv_file(csv_reader, target_model_name)

