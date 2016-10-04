from django.core.management.base import BaseCommand, CommandError
from apella.models import Position
from optparse import make_option


class Command(BaseCommand):
    help = 'Post a position'
    args = '<position id>'

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
        if len(args) != 1:
            raise CommandError("Invalid number of arguments")
        position_id = args[0]
        starts_at = options['starts_at']
        ends_at = options['ends_at']

        try:
            position = Position.objects.get(id=position_id)
            position.starts_at = starts_at
            position.ends_at = ends_at
            position.state = '2'
            position.save()
            self.stdout.write("Posted position %s" % position_id)
        except ValueError:
            raise CommandError("Position id must be an integer")
        except ValidationError as ve:
            raise CommandError(ve)
        except Position.DoesNotExist:
            raise CommandError("Position %s does not exist" % position_id)
