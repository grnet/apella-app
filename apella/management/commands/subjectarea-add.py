from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from apella.management.utils import ApellaCommand
from apella.models import SubjectArea, MultiLangFields


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
            title = MultiLangFields.objects.create(
                    el=title_el, en=title_en)
            subject_area = SubjectArea.objects.create(title=title)

            self.stdout.write(
                "Created subject area %s : %s" %
                (subject_area.pk, subject_area.title.el))
        except BaseException, e:
            raise CommandError(e)
        except:
            self.stdout.write("Operation failed")
