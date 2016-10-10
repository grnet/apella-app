from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from apella.management.utils import ApellaCommand
from apella.models import Department, School, Institution,\
    DepartmentEl, DepartmentEn


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
            department_el = DepartmentEl.objects.create(title=title_el)
            institution = Institution.objects.get(id=institution_id)
            school = School.objects.get(id=school_id)
            department = Department.objects.create(
                                            institution=institution,
                                            school=school,
                                            el=department_el)
            if title_en:
                department_en = DepartmentEn.objects.create(title=title_en)
                department.en = department_en
                department.save()

            self.stdout.write(
                "Created department %s : %s" %
                (department.pk, department_el.title))
        except School.DoesNotExist:
            raise CommandError("School %s does not exist" % school_id)
        except Institution.DoesNotExist:
            raise CommandError(
                "Institution %s does not exist" % institution_id)
        except BaseException, e:
            raise CommandError(e)
