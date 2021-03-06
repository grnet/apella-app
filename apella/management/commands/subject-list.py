from django.core.management.base import BaseCommand, CommandError
from apella.models import Subject


class Command(BaseCommand):
    help = 'List positions'

    def handle(self, *args, **options):
        if args:
            raise CommandError("Command does not accept any arguments")

        subjects = Subject.objects.all()
        if subjects:
            self.stdout.write('ID\tTitle\tArea\tOld Code')
        for subject in subjects:
            self.stdout.write(
                '%s\t%s\t%s (%s)\t%s' %
                (subject.id, subject.title.el, subject.area.title.el,
                    subject.area.id, subject.old_code))
