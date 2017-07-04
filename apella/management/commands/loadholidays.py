import json
from apella.management.utils import LoadDataCommand, smart_locale_unicode


class Command(LoadDataCommand):

    def handle(self, *args, **options):

        file_path = options['csv_file']
        with open(file_path) as csv_file:

            success = 0
            res = []

            for record in csv_file:
                date, reason_el, _,  _, _ = \
                    self.preprocess(record)

                if reason_el:
                    el = dict({'date': date, 'reason_el': reason_el})
                    res.append(el)
                    success = success + 1

            output = json.dumps(res, ensure_ascii=False, indent=4)
            self.stdout.write(smart_locale_unicode(output) + "\n")

