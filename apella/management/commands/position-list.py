from django.core.management.base import CommandError
from apella.management.utils import ApellaCommand
from apella.models import Position
from apella import common


class Command(ApellaCommand):
    help = 'List positions'

    def handle(self, *args, **options):
        if args:
            raise CommandError("Command does not accept any arguments")

        positions = Position.objects.all()
        if positions:
            self.stdout.write('ID\tTitle\tAuthor\tState')
        for position in positions:
            p_state = [str(p[1]) for p in common.POSITION_STATES
                       if p[0] == position.state]
            self.stdout.write('%s\t%s\t%s\t%s (%s)' % (
                position.id, position.title, position.author, position.state,
                p_state[0]))
