from django.core.management.base import BaseCommand, CommandError
from apella.models import ApellaUser, Position


class Command(BaseCommand):
    help = 'Create a position with the given title and author'
    args = '<title> <author id>'

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError("Invalid number of arguments")
        title, author = args[:2]

        try:
            position_author = ApellaUser.objects.get(id=author)
            if position_author.role != '1':
                raise CommandError(
                    "Only institution managers are allowed to create" +
                    "new positions")
            p = Position.objects.create(title=title, author=position_author)
            self.stdout.write(
                "Created position %s : title = %s author = %s" %
                (p.pk, title, position_author.username))
        except ValueError:
            raise CommandError("Author id must be an integer")
        except ApellaUser.DoesNotExist:
            raise CommandError("User %s does not exist" % author)
