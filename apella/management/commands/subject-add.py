from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from apella.management.utils import ApellaCommand
from apella.models import SubjectArea, Subject, SubjectEl, SubjectEn


class Command(ApellaCommand):
    help = 'Create a subject'
    args = '<title el> <subject area id>'

    option_list = BaseCommand.option_list + (
        make_option('--en',
                    dest='en',
                    help='Subject title in english'),
        )

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError("Invalid number of arguments")
        title_el, subject_area_id = args[:2]
        title_el = title_el
        title_en = options['en']

        try:
            subject_area = SubjectArea.objects.get(id=subject_area_id)
            subject_el = SubjectEl.objects.create(title=title_el)
            subject = Subject.objects.create(area=subject_area, el=subject_el)

            if title_en:
                subject_en = SubjectEn.objects.create(title=title_en)
                subject.en = subject_en
                subject.save()

            self.stdout.write(
                    "Created subject %s : %s, area : %s" %
                    (subject.pk, subject_el.title, subject.area.el.title))
        except SubjectArea.DoesNotExist:
            raise CommandError(
                "Subject area %s does not exist" % subject_area_id)
        except ValueError:
            raise CommandError(
                "Expected integer for <subject area id>, got: %s" %
                subject_area_id)
        except:
            raise
