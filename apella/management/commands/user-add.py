import os
import json

from django.core.management.base import CommandError
from django.db.utils import IntegrityError
from rest_framework.authtoken.models import Token
from apella.management.utils import ApellaCommand
from apella.models import ApellaUser, MultiLangFields
from apella import common


class Command(ApellaCommand):
    help = 'Create a user'

    def add_arguments(self, parser):

        parser.add_argument(
            '--username',
            dest='username',
            help='Unique user name',
        )

        parser.add_argument(
            '--password-from-json',
            dest='password_from_json',
            help='Read password using the username as key in this json file',
        )

        parser.add_argument(
            '--first-name-el',
            dest='first_name_el',
            help='First name in Greek',
        )

        parser.add_argument(
            '--last-name-el',
            dest='last_name_el',
            help='Last name in Greek',
        )

        parser.add_argument(
            '--father-name-el',
            dest='father_name_el',
            help='',
        )

        parser.add_argument(
            '--first-name-en',
            dest='first_name_en',
            help='First name in english',
        )

        parser.add_argument(
            '--last-name-en',
            dest='last_name_en',
            help='Last name in english',
        )

        parser.add_argument(
            '--father-name-en',
            help='Father name in english',
        )

        parser.add_argument(
            '--email',
            dest='email',
            help='Email')

        parser.add_argument(
            '--role',
            dest='role',
            default='2',
            choices=[x[0] for x in common.USER_ROLES],
            help='Choose a role for the user')

    def handle(self, *args, **options):

        password_from_json = options['password_from_json']
        if not password_from_json:
            password_from_json = os.environ['APELLA_PASSWORD_FROM_JSON']

        if not password_from_json:
            raise CommandError(
                "Neither --password-from-json option "
                "nor APELLA_PASSWORD_FROM_JSON environment variable is present")

        try:
            with open(password_from_json) as password_file:
                data = json.load(password_file)
        except IOError as ioe:
            raise CommandError(ioe)

        username = options['username']
        if not username in data:
            m = "Cannot find %r in file %s" % (username, password_from_json)
            raise CommandError(m)

        password = data[username]
        first_name_el = options['first_name_el']
        last_name_el = options['last_name_el']
        father_name_el = options['father_name_el']
        first_name_en = options['first_name_en']
        last_name_en = options['last_name_en']
        father_name_en = options['father_name_en']

        first_name = MultiLangFields.objects.create(
                el=first_name_el, en=first_name_en)
        last_name = MultiLangFields.objects.create(
                el=last_name_el, en=last_name_en)
        father_name = MultiLangFields.objects.create(
                el=father_name_el, en=father_name_en)

        try:
            a = ApellaUser.objects.create_user(
                    username=username,
                    password=password,
                    role=options['role'],
                    email=options['email'],
                    first_name=first_name,
                    last_name=last_name,
                    email_verified=True,
                    father_name=father_name)
        except IntegrityError as e:
            raise CommandError(e.message)

        token = Token.objects.create(user=a)

        self.stdout.write(
            "User with id: %s, role: %s, token:%s created" %
            (a.pk, options['role'], token))
