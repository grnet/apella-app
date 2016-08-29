from django.core.management.base import BaseCommand, CommandError
from apella.models import ApellaUser, Position, Candidacy


class Command(BaseCommand):
    help = 'Create a candidacy for a position for the given user'
    args = '<position id> <candidate id>'

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError("Invalid number of arguments")
        position_id, candidate_id = args[:2]

        try:
            position = Position.objects.get(id=position_id)
            candidate = ApellaUser.objects.get(id=candidate_id)
            c = Candidacy.objects.create(
                    position=position, candidate=candidate)
            self.stdout.write(
                "Created candidacy %s : candidate = %s position = %s" %
                (c.pk, c.candidate.username, c.position.id))
        except ValueError:
            raise CommandError("Position id and candidate id must be integers")
        except Position.DoesNotExist:
            raise CommandError("Position %s does not exist" % position_id)
        except ApellaUser.DoesNotExist:
            raise CommandError("User %s does not exist" % candidate_id)
