from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from apella.management.utils import ApellaCommand
from apella.models import Institution, School, MultiLangFields


class Command(ApellaCommand):
    help = 'Create a school for the given institution'
    args = '<institution id> <title el>'

    option_list = BaseCommand.option_list + (
        make_option('--en',
                    dest='en',
                    help='School title in english'),
        )

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError("Invalid number of arguments")
        institution_id, title_el = args[:2]
        title_en = options['en']

        try:
            institution = Institution.objects.get(id=institution_id)
            title = MultiLangFields.objects.create(
                    el=title_el, en=title_en)
            school = School.objects.create(
                institution=institution, title=title)

            self.stdout.write(
                "Created school %s : %s for institution: %s" %
                (school.pk, school.title.el, school.institution.id))
        except Institution.DoesNotExist:
            raise CommandError(
                "Institution %s does not exist" % institution_id)
        except BaseException, e:
            raise CommandError(e)
        except:
            self.stdout.write("Operation failed")
