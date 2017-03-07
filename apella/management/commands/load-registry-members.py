import csv

from django.core.management.base import CommandError
from django.db.utils import IntegrityError

from apella.models import Department, Registry, Professor, \
    ApellaUser
from apella.management.utils import ApellaCommand
from apella import common


class Command(ApellaCommand):
    help = 'Create or update a registry of the given type'

    def add_arguments(self, parser):
        parser.add_argument('csv_file')
        parser.add_argument('--department-id',
                            dest='department_id',
                            help='Department id')

        parser.add_argument('--type',
                            dest='registry_type',
                            help='Registry type: internal, external')

    def handle(self, *args, **options):
        department_id = options['department_id']
        registry_type = options['registry_type']
        csv_file_path = options['csv_file']

        types = [x[0] for x in common.REGISTRY_TYPES]
        if registry_type not in types:
            raise CommandError(
                    "Invalid <type> argument. Type must be in %s" %
                    types)
        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            raise CommandError(
                "Department %s does not exist" % department_id)

        users = []
        with open(csv_file_path) as f:
            csv_reader = csv.reader(f)
            csv_iterator = iter(csv_reader)
            for user_id in csv_iterator:
                uid = int(user_id[0])
                try:
                    u = ApellaUser.objects.get(id=uid)
                    users.append(u.professor)
                except ApellaUser.DoesNotExist:
                    raise CommandError(
                        "ApellaUser does not exist, user_id : %r" % uid)
                except Professor.DoesNotExist:
                    raise CommandError(
                        "Professor does not exist, user_id : %r" % uid)

        try:
            registry = Registry.objects.get(
                    department=department, type=registry_type)
        except Registry.DoesNotExist:
            registry = Registry.objects.create(
                department=department, type=registry_type)

        for u in users:
            if u not in registry.members.all():
                registry.members.add(u)
                self.stdout.write('adding user %r to registry %r' %
                    (u.user.id, registry.id))
        registry.save()
