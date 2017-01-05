from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from apella.models import ApellaUser, Candidate
from apella import common
from apella.management.utils import get_user, ApellaCommand


class Command(ApellaCommand):
    help = 'Create a candidate from an existing user'
    args = '<user id or username>'

    def add_arguments(self, parser):
        parser.add_argument('user_id_or_username')

    def handle(self, *args, **options):
        user_id_or_username = options['user_id_or_username']

        try:
            user = get_user(user_id_or_username)
            a = Candidate.objects.create(user=user, is_verified=True)

            self.stdout.write("Candidate with id: %s created" % a.pk)
        except ApellaUser.DoesNotExist:
            raise CommandError("User %s does not exist" % user_id_or_username)
