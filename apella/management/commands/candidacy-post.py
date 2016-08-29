from django.core.management.base import BaseCommand, CommandError
from apella.models import Candidacy
from datetime import datetime


class Command(BaseCommand):
    help = 'Post a candidacy'
    args = '<candidacy id>'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Invalid number of arguments")
        candidacy_id = args[0]

        try:
            candidacy = Candidacy.objects.get(id=candidacy_id)
            if candidacy.state != '1':
                raise CommandError(
                        "Cannot post candidacy, invalid initial state")
            candidacy.state = '2'
            candidacy.submitted_at = datetime.now()
            candidacy.save()
        except ValueError:
            raise CommandError("Candidacy id must be an integer")
        except Candidacy.DoesNotExist:
            raise CommandError("Candidacy %s does not exist" % candidacy_id)
