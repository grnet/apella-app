from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.utils import IntegrityError
from apella.models import Department, Registry, ApellaUser
from apella.management.utils import get_user


class Command(BaseCommand):
    help = 'Create a registry of the given type ' + \
        str([str(x[0]) + ':' + str(x[1]) for x in Registry.TYPES]).strip('[]')
    args = '<department_id> <type>'

    option_list = BaseCommand.option_list + (
        make_option('--members',
                    dest='members',
                    help='Set registry members'),
    )

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError("Invalid number of arguments")
        department_id, type = args[:2]
        members = options['members']

        types = [x[0] for x in Registry.TYPES]
        if str(type) not in types:
            raise CommandError(
                    "Invalid <type> argument. Type must be in %s" %
                    str(Registry.TYPES))
        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            raise CommandError("Department %s does not exist" % department_id)

        users = []
        if members:
            try:
                user_ids = members.split(',')
                for user_id in user_ids:
                    users.append(get_user(user_id))
            except ApellaUser.DoesNotExist:
                raise CommandError("User with id %s does not exist" % user_id)

        try:
            with transaction.atomic():
                registry = Registry.objects.create(
                        department=department, type=type)
                registry.members = users
                registry.save()
            self.stdout.write(
                "Created registry %s for department %s, type %s" %
                (registry.pk, registry.department.title, registry.type))
        except IntegrityError:
            raise CommandError(
                "Unique constraint failed. There is already" +
                " a registry of type %s for department %s" %
                (type, department_id))
