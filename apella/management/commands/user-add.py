from django.core.management.base import CommandError
from django.contrib.auth.models import Group
from apella.management.utils import ApellaCommand
from apella.models import ApellaUser, ApellaUserEl, ApellaUserEn
from apella import common


class Command(ApellaCommand):
    help = 'Create a user'
    args = '<username> <password>'

    def add_arguments(self, parser):
        parser.add_argument('username')
        parser.add_argument('password')

        parser.add_argument('first_name_el')
        parser.add_argument('last_name_el')
        parser.add_argument('father_name_el')
        parser.add_argument(
            '--first_name_en',
            dest='first_name_en',
            help='First name in english')
        parser.add_argument(
            '--last_name_en',
            dest='last_name_en',
            help='Last name in english')
        parser.add_argument(
            '--father_name_en',
            dest='father_name_en',
            help='Father name in english')
        parser.add_argument(
            '--email',
            dest='email',
            help='Email')
        parser.add_argument(
            '--group_name',
            dest='group_name',
            help='Group name')
        parser.add_argument(
            '--role',
            dest='role',
            default='2',
            choices=[x[0] for x in common.USER_ROLES],
            help='Choose a role for the user')

    def handle(self, *args, **options):

        username = options['username']
        password = options['password']
        first_name_el = options['first_name_el']
        last_name_el = options['last_name_el']
        father_name_el = options['father_name_el']
        first_name_en = options['first_name_en']
        last_name_en = options['last_name_en']
        father_name_en = options['father_name_en']
        group_name = options['group_name']

        try:
            if group_name:
                group, created = Group.objects.get_or_create(
                                    name=group_name)
                if created:
                    self.stdout.write("New group with name: %s created"
                                      % group.name)

            el = ApellaUserEl.objects.create(
                first_name=first_name_el,
                last_name=last_name_el,
                father_name=father_name_el)
            en = ApellaUserEn.objects.create(
                first_name=first_name_en,
                last_name=last_name_en,
                father_name=father_name_en)

            a = ApellaUser.objects.create_user(
                    username=username,
                    password=password,
                    role=options['role'],
                    email=options['email'],
                    el=el,
                    en=en)

            self.stdout.write("User with id: %s created" % a.pk)

            if group_name and group:
                a.groups.add(group)
                self.stdout.write("Group %s added to user %s"
                                   % (group.name, a.pk))

        except BaseException as e:
                raise CommandError(e)
