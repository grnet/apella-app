from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from apella.management.utils import ApellaCommand
from apella.models import Department, School, Institution,\
    MultiLangFields


class Command(ApellaCommand):
    help = 'Create a department for the given school'
    args = '<institution id> <school id> <title el>'

    option_list = BaseCommand.option_list + (
        make_option('--en',
                    dest='en',
                    help='Department title in english'),
        )

    def handle(self, *args, **options):
        if len(args) != 3:
            raise CommandError("Invalid number of arguments")
        institution_id, school_id, title_el = args[:3]
        title_en = options['en']

        try:
            title = MultiLangFields.objects.create(
                    el=title_el, en=title_en)
            institution = Institution.objects.get(id=institution_id)
            school = School.objects.get(id=school_id)
            department = Department.objects.create(
                                            institution=institution,
                                            school=school,
                                            title=title,
                                            dep_number=20)
            self.stdout.write(
                "Created department %s : %s" %
                (department.pk, department.title.el))
        except School.DoesNotExist:
            raise CommandError("School %s does not exist" % school_id)
        except Institution.DoesNotExist:
            raise CommandError(
                "Institution %s does not exist" % institution_id)
        except BaseException, e:
            raise CommandError(e)
