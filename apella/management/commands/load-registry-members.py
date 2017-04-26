import csv

from django.core.management.base import CommandError
from django.db.utils import IntegrityError

from apella.models import Department, Registry, Professor, \
    ApellaUser
from apella.management.utils import ApellaCommand
from apella import common
from apella.serializers.mixins import send_registry_emails


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
        parser.add_argument('--old-ids',
                            dest='old_ids',
                            default=False,
                            help='csv file contains old user ids')

    def handle(self, *args, **options):
        department_id = options['department_id']
        registry_type = options['registry_type']
        csv_file_path = options['csv_file']
        old_ids = options['old_ids']

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
                    if not old_ids:
                        u = ApellaUser.objects.get(id=uid)
                    else:
                        u = ApellaUser.objects.get(old_user_id=uid)
                except ApellaUser.DoesNotExist:
                    self.stdout.write(
                        "ApellaUser does not exist, user_id : %r" % uid)
                    continue
                try:
                    p = u.professor
                    if not p.is_verified:
                        self.stdout.write(
                            "Professor profile unverified, user_id : %r" %
                            uid)
                        continue
                    users.append(p)
                except Professor.DoesNotExist:
                    self.stdout.write(
                        "Professor does not exist, user_id : %r" % uid)
                    continue

        try:
            registry = Registry.objects.get(
                    department=department, type=registry_type)
        except Registry.DoesNotExist:
            registry = Registry.objects.create(
                department=department, type=registry_type)

        new_members = []
        for u in users:
            if u not in registry.members.all():
                registry.members.add(u)
                new_members.append(u)
                self.stdout.write(
                    'adding user %r to registry %r' %
                    (u.user.id, registry.id))
        registry.save()
        send_registry_emails(new_members, department)
