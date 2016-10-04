from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from apella.management.utils import ApellaCommand
from apella.models import Institution, InstitutionEl, InstitutionEn


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
            institution_el = InstitutionEl.objects.create(title=title_el)
            institution = Institution.objects.create(el=institution_el)

            if title_en:
                institution_en = InstitutionEn.objects.create(title=title_en)
                institution.en = institution_en
                institution.save()

            self.stdout.write(
                "Created institution %s : %s" %
                (institution.pk, institution_el.title))
        except BaseException, e:
            raise CommandError(e)
        except:
            self.stdout.write("Operation failed")
