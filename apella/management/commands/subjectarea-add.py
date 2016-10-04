from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from apella.management.utils import ApellaCommand
from apella.models import SubjectArea, SubjectAreaEl, SubjectAreaEn


class Command(ApellaCommand):
    help = 'Create a subject area'
    args = '<title el>'

    option_list = BaseCommand.option_list + (
        make_option('--en',
                    dest='en',
                    help='Subject area title in english'),
        )

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Invalid number of arguments")
        title_el = args[0]
        title_en = options['en']

        try:
            subject_area_el = SubjectAreaEl.objects.create(title=title_el)
            subject_area = SubjectArea.objects.create(el=subject_area_el)

            if title_en:
                subject_area_en = SubjectAreaEn.objects.create(title=title_en)
                subject_area.en = subject_area_en
                subject_area.save()

            self.stdout.write(
                "Created subject area %s : %s" %
                (subject_area.pk, subject_area_el.title))
        except BaseException, e:
            raise CommandError(e)
        except:
            self.stdout.write("Operation failed")
