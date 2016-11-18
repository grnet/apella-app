from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from rest_framework.authtoken.models import Token
from apella.management.utils import ApellaCommand
from apella.models import ApellaUser, MultiLangFields
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

            first_name = MultiLangFields.objects.create(
                    el=first_name_el, en=first_name_en)
            last_name = MultiLangFields.objects.create(
                    el=last_name_el, en=last_name_en)
            father_name = MultiLangFields.objects.create(
                    el=father_name_el, en=father_name_en)

            a = ApellaUser.objects.create_user(
                    username=username,
                    password=password,
                    role=options['role'],
                    email=options['email'],
                    first_name=first_name,
                    last_name=last_name,
                    father_name=father_name)
            token = Token.objects.create(user=a)

            self.stdout.write(
                "User with id: %s, token:%s created" % (a.pk, token))

            if group_name and group:
                a.groups.add(group)
                self.stdout.write(
                    "Group %s added to user %s" % (group.name, a.pk))

        except BaseException as e:
                raise CommandError(e)
