from django.db.models import ProtectedError

from apella import common
from apella.models import Institution, MultiLangFields
from apella.management.utils import LoadDataCommand, smart_locale_unicode


class Command(LoadDataCommand):

    MODEL = Institution

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)

    def handle(self, *args, **options):
        file_path = options['csv_file']
        ircids = []
        with open(file_path) as csv_file:
            success = 0
            failed = 0
            renamed = 0
            deleted = 0
            for institution_record in csv_file:
                ircid, title_el, title_en, category_str = \
                    self.preprocess(institution_record)

                try:
                    ircid = int(ircid)
                    ircids.append(ircid)
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

                if Institution.objects.filter(id=ircid).exists():
                    institution = Institution.objects.get(id=ircid)
                    title = institution.title
                    title_el_before = title.el
                    title_en_before = title.en
                    title.el = title_el
                    title.en = title_en
                    title.save()
                    self.stdout.write(
                        "Renamed institution %s from %s, %s to %s, %s" %
                        (ircid, title_el_before, title_en_before,
                            title.el, title.en))
                    renamed += 1
                    continue

                title = MultiLangFields.objects.create(
                        el=title_el, en=title_en)
                institution_data = {
                        'id': ircid,
                        'title': title,
                        'category': category[0]
                }
                Institution.objects.create(**institution_data)
                success += 1
                self.stdout.write(
                    "%s %s is created." % (ircid, title_el))

            missing = Institution.objects.exclude(id__in=ircids)
            if missing:
                deleted_ids = []
                for institution in missing:
                    try:
                        d_id = institution.id
                        institution.title.delete()
                        institution.delete()
                        deleted_ids.append(d_id)
                        deleted += 1
                    except ProtectedError:
                        self.stdout.write(
                            "\nProtectedError: Could not delete institution %s"
                            % institution.id)

            if success > 0:
                self.stdout.write(
                    "\nSuccessfully created %d institutions" % success)
            if renamed > 0:
                self.stdout.write(
                    "\nSuccessfully renamed %d institutions" % renamed)
            if deleted > 0:
                self.stdout.write(
                    "\n%d deleted, [%s]" %
                    (deleted, ','.join(str(x) for x in deleted_ids)))
            if failed > 0:
                self.stdout.write("\n%d failed" % failed)
