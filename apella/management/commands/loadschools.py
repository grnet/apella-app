from django.core.management.base import CommandError
from django.db import IntegrityError

from apella import common
from apella.models import Institution, School, SchoolEl, SchoolEn
from apella.management.utils import LoadDataCommand, smart_locale_unicode


class Command(LoadDataCommand):

    MODEL = School

    def handle(self, *args, **options):

        file_path = options['csv_file']
        with open(file_path) as csv_file:

            success = 0
            failed = 0
            for school_record in csv_file:
                ircid, institution_title_el, institution_title_en,\
                    school_id, school_title_el, school_title_en = \
                    self.preprocess(school_record)

                try:
                    school_id = int(school_id)
                except ValueError:
                    self.stdout.write(
                        "----- Could not parse school id : %s" % school_id)
                    failed += 1
                    continue

                school_title_el = smart_locale_unicode(school_title_el)
                school_title_en = smart_locale_unicode(school_title_en)
                if school_title_el == '-':
                    continue

                school_el = SchoolEl.objects.create(title=school_title_el)
                school_en = SchoolEn.objects.create(title=school_title_en)

                try:
                    institution = Institution.objects.get(id=ircid)
                except Institution.DoesNotExist:
                    self.stdout.write(
                        "----- Could not parse institution id %s" % ircid)
                    failed += 1
                    continue

                school_data = {
                        'institution': institution,
                        'el': school_el,
                        'en': school_en,
                        'id': school_id
                }
                try:
                    school_obj = School.objects.create(**school_data)
                    success += 1
                    self.stdout.write(
                        "%s %s is created." % (school_id, school_title_el))
                except IntegrityError:
                    self.stdout.write("School %s already exists" % school_id)
                    failed += 1

            self.stdout.write(
                "\nSuccessfully created %d schools" % success)
            if failed > 0:
                self.stdout.write("%d failed" % failed)