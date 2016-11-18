from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from apella.management.utils import ApellaCommand
from apella.models import Institution, MultiLangFields


class Command(ApellaCommand):
    help = 'Create an institution'
    args = '<title el>'

    option_list = BaseCommand.option_list + (
        make_option('--en',
                    dest='en',
                    help='Institution title in english'),
        )

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Invalid number of arguments")
        title_el = args[0]
        title_en = options['en']

        try:
            title = MultiLangFields.objects.create(
                    el=title_el, en=title_en)
            institution = Institution.objects.create(title=title)

            self.stdout.write(
                "Created institution %s : %s" %
                (institution.pk, institution.title.el))
        except BaseException, e:
            raise CommandError(e)
        except:
            self.stdout.write("Operation failed")
