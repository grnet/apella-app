from django.core.management.base import BaseCommand, CommandError
from apella.models import Candidacy


class Command(BaseCommand):
    help = 'List candidacies'

    def handle(self, *args, **options):
        if args:
            raise CommandError("Command does not accept any arguments")

        candidacies = Candidacy.objects.all()
        if candidacies:
            self.stdout.write('ID\tCandidate\tPosition\tSubmitted at\tState')
        for candidacy in candidacies:
            c_state = [str(c[1]) for c in Candidacy.STATES
                       if c[0] == candidacy.state]
            self.stdout.write('%s\t%s\t%s\t%s\t%s (%s)' % (
                candidacy.pk, candidacy.candidate.username,
                candidacy.position.title, candidacy.submitted_at,
                candidacy.state, c_state[0]))
