from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from apella.models import ApellaUser, Position, Department,\
        Subject, SubjectArea
from apella.management.utils import get_user

from optparse import make_option


class Command(BaseCommand):
    help = 'Create a position with the given title and author'
    args = '<title> <author id or username> <department id> <description>' + \
        ' <subject area> <subject> <fek url> <fek posted at>'

    option_list = BaseCommand.option_list + (
        make_option('--start',
                    dest='starts_at',
                    help='The date and time the position starts accepting' +
                    ' candidacies.'),
        make_option('--end',
                    dest='ends_at',
                    help='The date and time the position stops accepting' +
                    ' candidacies.'),
                        )

    def handle(self, *args, **options):
        if len(args) != 8:
            raise CommandError("Invalid number of arguments")

        title, author, department_id, description, \
            subject_area_id, subject_id, fek, fek_posted_at = args[:8]
        # TODO: validate dates
        starts_at = options['starts_at']
        ends_at = options['ends_at']

        try:
            position_author = get_user(author)
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
                (p.pk, p.title, p.author.username))
        except ValidationError as ve:
            raise CommandError(ve)
        except ApellaUser.DoesNotExist:
            raise CommandError("User %s does not exist" % author)
        except Department.DoesNotExist:
            raise CommandError("Department %s does not exist" % department_id)
        except Subject.DoesNotExist:
            raise CommandError("Subject %s does not exist" % subject_id)
