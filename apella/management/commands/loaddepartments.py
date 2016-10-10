from django.core.management.base import CommandError
from django.db import IntegrityError

from apella import common
from apella.models import Institution, School, Department, DepartmentEl,\
    DepartmentEn
from apella.management.utils import LoadDataCommand, smart_locale_unicode


class Command(LoadDataCommand):

    MODEL = Department

    def handle(self, *args, **options):

        file_path = options['csv_file']
        with open(file_path) as csv_file:

            success = 0
            failed = 0
            for school_record in csv_file:
                ircid, institution_title_el, institution_title_en,\
                    school_id, school_title_el, school_title_en,\
                    diid, department_title_el, department_title_en =\
                    self.preprocess(school_record)

                try:
                    diid = int(diid)
                except ValueError:
                    self.stdout.write(
                        "---- Could not parse department id : %s" % diid)
                    failed += 1
                    continue

                department_title_el = smart_locale_unicode(department_title_el)
                department_title_en = smart_locale_unicode(department_title_en)
                if department_title_el == '-':
                    continue

                department_el = DepartmentEl.objects.create(
                    title=department_title_el)
                department_en = DepartmentEn.objects.create(
                    title=department_title_en)

                institution = Institution.objects.get(id=ircid)
                try:
                    school = School.objects.get(id=school_id)
                except School.DoesNotExist:
                    if school_title_el == '-':
                        school = None
                    else:
                        failed += 1
                        self.stdout.write(
                            "School %s does not exist" % school_id)
                        continue

                department_data = {
                        'institution': institution,
                        'el': department_el,
                        'en': department_en,
                        'id': diid,
                        'school': school}

                try:
                    department = Department.objects.create(**department_data)
                    success += 1
                    self.stdout.write(
                        "%s %s is created." % (diid, department_title_el))
                except IntegrityError:
                    self.stdout.write("Department %s already exists" % diid)
                    failed += 1

            self.stdout.write(
                "\nSuccessfully created %d departments" % success)
            if failed > 0:
                self.stdout.write("%d failed" % failed)
