from django.db import IntegrityError

from apella.models import SubjectArea, Subject, MultiLangFields
from apella.management.utils import LoadDataCommand, smart_locale_unicode


class Command(LoadDataCommand):

    MODEL = SubjectArea

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--delete-all',
            dest='delete',
            default=False,
            help='Delete subject areas, subjects')

    def handle(self, *args, **options):

        if options['delete']:
            SubjectArea.objects.all().delete()
            Subject.objects.all().delete()

        file_path = options['csv_file']
        with open(file_path) as csv_file:

            success_subjectareas = 0
            failed_subjectareas = 0
            success_subjects = 0
            failed_subjects = 0

            for record in csv_file:
                rid, title_el, title_en = \
                    self.preprocess(record)

                title_el = smart_locale_unicode(title_el)
                title_en = smart_locale_unicode(title_en)

                if rid.isdigit():
                    sa_id = int(rid)

                    title = MultiLangFields.objects.create(
                            el=title_el, en=title_en)

                    subjectarea_data = {
                            'id': sa_id,
                            'title': title,
                    }
                    try:
                        SubjectArea.objects.create(**subjectarea_data)
                        success_subjectareas += 1
                        self.stdout.write(
                            "%s %s is created." % (sa_id, title_el))
                    except IntegrityError:
                        self.stdout.write("Subject Area %s already exists"
                                          % sa_id)
                        failed_subjectareas += 1

                else:
                    try:
                        sa_id, s_id = map(lambda x: int(x), rid.split('.'))

                        try:
                            area = SubjectArea.objects.get(id=sa_id)
                        except SubjectArea.DoesNotExist:
                            self.stdout.write(
                                "Could not find subject area  %s" % sa_id)
                            failed_subjects += 1
                            continue

                        title = MultiLangFields.objects.create(
                            el=title_el, en=title_en)

                        subject_data = {
                                'area': area,
                                'title': title
                        }

                        try:
                            Subject.objects.create(**subject_data)
                            success_subjects += 1
                            self.stdout.write(
                                "%s %s is created." % (s_id, title_el))
                        except IntegrityError:
                            self.stdout.write("Subject %s already exists"
                                              % s_id)
                            failed_subjects += 1

                    except ValueError:
                        self.stdout.write(
                            "---- Could not parse record : %s" % rid)
                        failed_subjects += 1
                        continue

            self.stdout.write(
                "\nSuccessfully created %d subject areas and %d subjects"
                % (success_subjectareas, success_subjects))
            if failed_subjectareas > 0:
                self.stdout.write("%d subject areas failed"
                                  % failed_subjectareas)
