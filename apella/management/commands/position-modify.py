from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from apella.models import ApellaUser, Position


class Command(BaseCommand):
    help = 'Update a position'
    args = '<position ID>'

    option_list = BaseCommand.option_list + (
        make_option('--set-elected',
                    dest='elected',
                    help='Choose an elected for the position'),
        )

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Please provide a position ID")
        position_id = args[0]
        elected = options['elected']

        if position_id.isdigit():
            try:
                position = Position.objects.get(id=int(position_id))
            except Position.DoesNotExist:
                raise CommandError("Invalid position ID")
        else:
            raise CommandError("Position ID must be an integer")

        if elected:
            if elected.isdigit():
                try:
                    elected = ApellaUser.objects.get(id=int(elected))
                    position.elected = elected
                    position.save()
                except ApellaUser.DoesNotExist:
                    raise CommandError("Invalid elected ID")
                except:
                    raise CommandError("Operation failed")

            else:
                raise CommandError("Elected ID must be an integer")



