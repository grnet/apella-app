from apella.management.utils import ApellaCommand
from django.core.management.base import CommandError
from django.contrib.auth.models import Group


class Command(ApellaCommand):
    help = 'Create a group'
    args = '<name>'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Invalid number of arguments")
        name = args[0]

        try:
            group = Group.objects.create(name=name)

            self.stdout.write(
                "Created group %s : %s" %
                (group.pk, group.name))
        except BaseException as e:
            raise CommandError(e)
