from django.core.management.base import CommandError
from django.db import IntegrityError

from apella import common
from apella.models import Institution, InstitutionEl, InstitutionEn,\
    Department, DepartmentEn, DepartmentEl, School, SchoolEn, SchoolEl
from apella.management.utils import LoadDataCommand, smart_locale_unicode


class Command(LoadDataCommand):

    MODEL = Institution

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--delete-all',
            dest='delete',
            default=False,
            help='Delete institutions, schools, departments')

    def handle(self, *args, **options):

        if options['delete']:
            Institution.objects.all().delete()
            InstitutionEl.objects.all().delete()
            InstitutionEn.objects.all().delete()
            School.objects.all().delete()
            SchoolEl.objects.all().delete()
            SchoolEn.objects.all().delete()
            Department.objects.all().delete()
            DepartmentEl.objects.all().delete()
            DepartmentEn.objects.all().delete()

        file_path = options['csv_file']
        with open(file_path) as csv_file:

            success = 0
            failed = 0
            for institution_record in csv_file:
                ircid, title_el, title_en, category_str = \
                    self.preprocess(institution_record)

                try:
                    ircid = int(ircid)
                except ValueError:
                    self.stdout.write(
                        "---- Could not parse institution id : %s" % ircid)
                    failed += 1
                    continue

                title_el = smart_locale_unicode(title_el)
                title_en = smart_locale_unicode(title_en)
                category_str = smart_locale_unicode(category_str)

                category = [key for key, value
                            in common.INSTITUTION_CATEGORIES
                            if category_str == key]

                if not category:
                    self.stdout.write(
                        "---- Unable to find institution category: %s" %
                        category_str)
                    failed += 1
                    continue

                institution_el = InstitutionEl.objects.create(title=title_el)
                institution_en = InstitutionEn.objects.create(title=title_en)

                institution_data = {
                        'id': ircid,
                        'el': institution_el,
                        'en': institution_en,
                        'category': category[0]
                }
                try:
                    institution = Institution.objects.create(
                        **institution_data)
                    success += 1
                    self.stdout.write(
                        "%s %s is created." % (ircid, title_el))
                except IntegrityError:
                    self.stdout.write("Institution %s already exists" % ircid)
                    failed += 1

            self.stdout.write(
                "\nSuccessfully created %d institutions" % success)
            if failed > 0:
                self.stdout.write("%d failed" % failed)
