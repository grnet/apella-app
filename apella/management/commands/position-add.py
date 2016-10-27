from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError

from apella.models import Position, Department, Subject, SubjectArea,\
    InstitutionManager
from apella.management.utils import ApellaCommand


class Command(ApellaCommand):
    help = 'Create a position'

    def add_arguments(self, parser):
        parser.add_argument('title')
        parser.add_argument('author')
        parser.add_argument('department_id')
        parser.add_argument('description')
        parser.add_argument('subject_area_id')
        parser.add_argument('subject_id')
        parser.add_argument('fek')
        parser.add_argument('fek_posted_at')
        parser.add_argument('starts_at')
        parser.add_argument('ends_at')
        parser.add_argument('discipline')

    def handle(self, *args, **options):
        title = options['title']
        author = options['author']
        department_id = options['department_id']
        description = options['description']
        discipline = options['discipline']
        subject_area_id = options['subject_area_id']
        subject_id = options['subject_id']
        fek = options['fek']
        fek_posted_at = options['fek_posted_at']
        starts_at = options['starts_at']
        ends_at = options['ends_at']

        try:
            position_author = InstitutionManager.objects.get(id=author)
            department = Department.objects.get(id=department_id)
            subject_area = SubjectArea.objects.get(id=subject_area_id)
            subject = Subject.objects.get(id=subject_id)

            p = Position.objects.create(
                    title=title, author=position_author,
                    department=department, description=description,
                    fek=fek, fek_posted_at=fek_posted_at,
                    subject_area=subject_area, discipline=discipline,
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
