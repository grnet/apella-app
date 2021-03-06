from django.core.management.base import CommandError
from apella.management.utils import ApellaCommand
from apella.models import Candidacy
from django.utils import timezone


class Command(ApellaCommand):
    help = 'Post a candidacy'
    args = '<candidacy id>'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Invalid number of arguments")
        candidacy_id = args[0]

        try:
            candidacy = Candidacy.objects.get(id=candidacy_id)
            candidacy.state = '2'
            candidacy.submitted_at = timezone.now()
            candidacy.save()
            self.stdout.write("Posted candidacy %s" % candidacy_id)
        except ValueError:
            raise CommandError("Candidacy id must be an integer")
        except Candidacy.DoesNotExist:
            raise CommandError("Candidacy %s does not exist" % candidacy_id)
