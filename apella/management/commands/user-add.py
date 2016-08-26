from django.core.management.base import BaseCommand, CommandError
from apella.models import ApellaUser

class Command(BaseCommand):
    help = 'Creates a user'
    args = '<username password>'

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError("Invalid number of arguments")
        username, password = args[:2]
        try:
            a= ApellaUser(username=username,password=password)
            a.save()
            self.stdout.write("User with id: %s created" % a.pk)
        except:
            self.stdout.write("Operation failed")
