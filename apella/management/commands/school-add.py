from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from apella.models import Institution, School


class Command(BaseCommand):
    help = 'Create a school for the given institution'
    args = '<institution id> <title>'

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError("Invalid number of arguments")
        institution_id, title = args[:2]

        try:
            institution = Institution.objects.get(id=institution_id)
            school = School.objects.create(
                title=title, institution=institution)
            self.stdout.write(
                "Created school %s : %s for institution: %s" %
                (school.pk, school.title, school.institution.title))
        except Institution.DoesNotExist:
            raise CommandError(
                "Institution %s does not exist" % institution_id)
        except BaseException, e:
            raise CommandError(e)
        except:
            self.stdout.write("Operation failed")
