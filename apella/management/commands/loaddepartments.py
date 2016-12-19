from django.db.models import ProtectedError

from apella.models import Institution, School, Department, MultiLangFields
from apella.management.utils import LoadDataCommand, smart_locale_unicode


class Command(LoadDataCommand):

    MODEL = Department

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)

    def handle(self, *args, **options):
        file_path = options['csv_file']
        diids = []
        with open(file_path) as csv_file:
            success = 0
            failed = 0
            renamed = 0
            deleted = 0
            for department_record in csv_file:
                ircid, institution_title_el, institution_title_en,\
                    school_id, school_title_el, school_title_en,\
                    diid, department_title_el, department_title_en =\
                    self.preprocess(department_record)

                try:
                    diid = int(diid)
                    diids.append(diid)
                except ValueError:
                    self.stdout.write(
                        "---- Could not parse department id : %s" % diid)
                    failed += 1
                    continue

                department_title_el = smart_locale_unicode(department_title_el)
                department_title_en = smart_locale_unicode(department_title_en)
                if department_title_el == '-':
                    continue

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

                if Department.objects.filter(id=diid).exists():
                    department = Department.objects.get(id=diid)
                    title = department.title
                    title_el_before = title.el
                    title_en_before = title.en
                    title.el = department_title_el
                    title.en = department_title_en
                    title.save()
                    self.stdout.write(
                        "Renamed department %s from %s, %s to %s, %s" %
                        (diid, title_el_before, title_en_before,
                            title.el, title.en))
                    renamed += 1
                    continue

                title = MultiLangFields.objects.create(
                    el=department_title_el, en=department_title_en)
                department_data = {
                        'institution': institution,
                        'title': title,
                        'id': diid,
                        'school': school}
                Department.objects.create(**department_data)
                success += 1
                self.stdout.write(
                    "%s %s is created." % (diid, department_title_el))

            missing = Department.objects.exclude(id__in=diids)
            if missing:
                deleted_ids = []
                for department in missing:
                    try:
                        d_id = department.id
                        department.title.delete()
                        department.delete()
                        deleted_ids.append(d_id)
                        deleted += 1
                    except ProtectedError:
                        self.stdout.write(
                            "\nProtectedError: Could not delete department %s"
                            % department.id)
            if success > 0:
                self.stdout.write(
                    "\nSuccessfully created %d departments" % success)
            if renamed > 0:
                self.stdout.write(
                    "\nSuccessfully renamed %d departments" % renamed)
            if deleted > 0:
                self.stdout.write(
                    "\n%d deleted, [%s]" %
                    (deleted, ','.join(str(x) for x in deleted_ids)))
            if failed > 0:
                self.stdout.write("%d failed" % failed)
