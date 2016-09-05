from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from apella.models import ApellaUser, Position, Institution
from apella.management.utils import get_user

from optparse import make_option


class Command(BaseCommand):
    help = 'Create a position with the given title and author'
    args = '<title> <author id or username> <institution id>'

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
        if len(args) != 3:
            raise CommandError("Invalid number of arguments")

        title, author, institution_id = args[:3]
        # TODO: validate dates
        starts_at = options['starts_at']
        ends_at = options['ends_at']

        try:
            position_author = get_user(author)
            institution = Institution.objects.get(id=institution_id)
            p = Position.objects.create(
                    title=title, author=position_author,
                    institution=institution,
                    starts_at=starts_at, ends_at=ends_at)
            self.stdout.write(
                "Created position %s : title = %s author = %s" %
                (p.pk, p.title, p.author.username))
        except ValidationError as ve:
            raise CommandError(ve)
        except ApellaUser.DoesNotExist:
            raise CommandError("User %s does not exist" % author)
