from django.db.models import ProtectedError

from apella.models import Institution, School, MultiLangFields
from apella.management.utils import LoadDataCommand, smart_locale_unicode


class Command(LoadDataCommand):

    MODEL = School

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)

    def handle(self, *args, **options):
        file_path = options['csv_file']
        ids = []
        with open(file_path) as csv_file:

            success = 0
            failed = 0
            renamed = 0
            deleted = 0
            for school_record in csv_file:
                ircid, institution_title_el, institution_title_en,\
                    school_id, school_title_el, school_title_en = \
                    self.preprocess(school_record)

                try:
                    school_id = int(school_id)
                    ids.append(school_id)
                except ValueError:
                    self.stdout.write(
                        "----- Could not parse school id : %s" % school_id)
                    failed += 1
                    continue

                title_el = smart_locale_unicode(school_title_el)
                title_en = smart_locale_unicode(school_title_en)
                if school_title_el == '-':
                    continue

                try:
                    institution = Institution.objects.get(id=ircid)
                except Institution.DoesNotExist:
                    self.stdout.write(
                        "----- Could not parse institution id %s" % ircid)
                    failed += 1
                    continue

                if School.objects.filter(id=school_id).exists():
                    school = School.objects.get(id=school_id)
                    title = school.title
                    title_el_before = title.el
                    title_en_before = title.en
                    title.el = title_el
                    title.en = title_en
                    title.save()
                    self.stdout.write(
                        "Renamed school %s from %s, %s to %s, %s" %
                        (school_id, title_el_before, title_en_before,
                            title.el, title.en))
                    renamed += 1
                    continue

                title = MultiLangFields.objects.create(
                        el=title_el, en=title_en)
                school_data = {
                        'institution': institution,
                        'title': title,
                        'id': school_id
                }
                School.objects.create(**school_data)
                success += 1
                self.stdout.write(
                    "%s %s is created." % (school_id, title_el))

            missing = School.objects.exclude(id__in=ids)
            if missing:
                deleted_ids = []
                for school in missing:
                    try:
                        d_id = school.id
                        school.title.delete()
                        school.delete()
                        deleted_ids.append(d_id)
                        deleted += 1
                    except ProtectedError:
                        self.stdout.write(
                            "\nProtectedError: Could not delete school %s"
                            % school.id)

            if success > 0:
                self.stdout.write(
                    "\nSuccessfully created %d schools" % success)
            if renamed > 0:
                self.stdout.write(
                    "\nSuccessfully renamed %d schools" % renamed)
            if deleted > 0:
                self.stdout.write(
                    "\n%d deleted, [%s]" %
                    (deleted, ','.join(str(x) for x in deleted_ids)))
            if failed > 0:
                self.stdout.write("%d failed" % failed)
