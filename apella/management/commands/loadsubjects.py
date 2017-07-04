from django.db.models import ProtectedError

from apella.models import SubjectArea, Subject, MultiLangFields
from apella.management.utils import LoadDataCommand, smart_locale_unicode


class Command(LoadDataCommand):

    MODEL = SubjectArea

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)

    def handle(self, *args, **options):
        file_path = options['csv_file']
        sa_ids = []
        with open(file_path) as csv_file:

            success_subjectareas = 0
            renamed_subjectareas = 0
            deleted_subjectareas = 0
            success_subjects = 0
            failed_subjects = 0
            renamed_subjects = 0

            for record in csv_file:
                rid, title_el, title_en = \
                    self.preprocess(record)

                title_el = smart_locale_unicode(title_el)
                title_en = smart_locale_unicode(title_en)

                if rid.isdigit():
                    sa_id = int(rid)
                    sa_ids.append(sa_id)

                    if SubjectArea.objects.filter(id=sa_id).exists():
                        sa = SubjectArea.objects.get(id=sa_id)
                        title = sa.title
                        sa_title_el_before = title.el
                        sa_title_en_before = title.en
                        title.el = title_el
                        title.en = title_en
                        title.save()
                        self.stdout.write(
                            "Renamed subject area %s from %s, %s to %s, %s" %
                            (sa_id, sa_title_el_before, sa_title_en_before,
                                title.el, title.en))
                        renamed_subjectareas += 1
                        continue

                    title = MultiLangFields.objects.create(
                            el=title_el, en=title_en)
                    subjectarea_data = {
                            'id': sa_id,
                            'title': title,
                    }
                    SubjectArea.objects.create(**subjectarea_data)
                    success_subjectareas += 1
                    self.stdout.write(
                        "%s %s is created." % (sa_id, title_el))

                else:
                    try:
                        sa_id, s_id = map(lambda x: int(x), rid.split('.'))
                    except ValueError:
                        self.stdout.write(
                            "---- Could not parse record : %s" % rid)
                        failed_subjects += 1
                        continue
                    try:
                        area = SubjectArea.objects.get(id=sa_id)
                    except SubjectArea.DoesNotExist:
                        self.stdout.write(
                            "Could not find subject area  %s" % sa_id)
                        failed_subjects += 1
                        continue

                    if Subject.objects.filter(
                            area=sa_id, title__el=title_el).exists():
                        s = Subject.objects.get(area=sa_id, title__el=title_el)
                        title = s.title
                        s_title_el_before = title.el
                        s_title_en_before = title.en
                        title.el = title_el
                        title.en = title_en
                        s.old_code = rid
                        title.save()
                        s.save()
                        self.stdout.write(
                            "Renamed subject %s from %s, %s to %s, %s" %
                            (s_id, s_title_el_before, s_title_en_before,
                                title.el, title.en))
                        renamed_subjects += 1
                        continue

                    title = MultiLangFields.objects.create(
                        el=title_el, en=title_en)

                    subject_data = {
                            'area': area,
                            'title': title,
                            'old_code': rid
                    }
                    Subject.objects.create(**subject_data)
                    success_subjects += 1
                    self.stdout.write(
                        "%s %s is created." % (s_id, title_el))

            missing = SubjectArea.objects.exclude(id__in=sa_ids)
            if missing:
                deleted_saids = []
                for sa in missing:
                    try:
                        d_id = sa.id
                        sa.title.delete()
                        sa.delete()
                        deleted_saids.append(d_id)
                        deleted_subjectareas += 1
                    except ProtectedError:
                        self.stdout.write(
                            "\nProtectedError: "
                            "Could not delete subject area %s"
                            % sa.id)

            if success_subjectareas > 0:
                self.stdout.write(
                    "\nSuccessfully created %d subject areas"
                    % success_subjectareas)
            if success_subjects > 0:
                self.stdout.write(
                    "\nSuccessfully created %d subjects"
                    % success_subjects)
            if renamed_subjectareas > 0:
                self.stdout.write(
                    "\nSuccessfully renamed %d subject areas"
                    % renamed_subjectareas)
            if renamed_subjects > 0:
                self.stdout.write(
                    "\nSuccessfully renamed %d subjects"
                    % renamed_subjects)
            if deleted_subjectareas > 0:
                self.stdout.write(
                    "\n%d subject areas deleted, [%s]" %
                    (deleted_subjectareas, ','.join(
                        str(x) for x in deleted_saids)))
            if failed_subjects > 0:
                self.stdout.write("%d subjects failed"
                                  % failed_subjects)
