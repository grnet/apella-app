from django.core.management.base import BaseCommand, CommandError
from apella.models import Position


class Command(BaseCommand):
    help = 'Post a position'
    args = '<position id>'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Invalid number of arguments")
        position_id = args[0]

        try:
            position = Position.objects.get(id=position_id)
            if position.state != '1':
                raise CommandError(
                        "Cannot post position, invalid initial state")
            position.state = '2'
            position.save()
        except ValueError:
            raise CommandError("Position id must be an integer")
        except Position.DoesNotExist:
            raise CommandError("Position %s does not exist" % position_id)
