from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from apella.models import Position, Department, Subject, SubjectArea,\
    InstitutionManager
from apella.management.utils import get_user, ApellaCommand

from optparse import make_option


class Command(ApellaCommand):
    help = 'Create a position with the given title and author'
    args = '<title> <author id> <department id> <description>' + \
        ' <subject area> <subject> <fek url> <fek posted at> <start> <end>'

    def handle(self, *args, **options):
        if len(args) != 10:
            raise CommandError("Invalid number of arguments")

        title, author, department_id, description,\
            subject_area_id, subject_id, fek, fek_posted_at,\
            starts_at, ends_at = args[:10]

        try:
            position_author = InstitutionManager.objects.get(id=author)
            department = Department.objects.get(id=department_id)
            subject_area = SubjectArea.objects.get(id=subject_area_id)
            subject = Subject.objects.get(id=subject_id)

            p = Position.objects.create(
                    title=title, author=position_author,
                    department=department, description=description,
                    fek=fek, fek_posted_at=fek_posted_at,
                    subject_area=subject_area,
                    subject=subject, starts_at=starts_at, ends_at=ends_at)

            self.stdout.write(
                "Created position %s : title = %s author = %s" %
                (p.pk, p.title, p.author.user.username))
        except ValidationError as ve:
            raise CommandError(ve)
        except InstitutionManager.DoesNotExist:
            raise CommandError(
                "Institution manager %s does not exist" % author)
        except Department.DoesNotExist:
            raise CommandError("Department %s does not exist" % department_id)
        except Subject.DoesNotExist:
            raise CommandError("Subject %s does not exist" % subject_id)
