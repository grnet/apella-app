from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from apella.util import urljoin


def send_new_credentials_to_old_users_email(old_users):
    BASE_URL = settings.BASE_URL or '/'
    login_url = urljoin(
        BASE_URL, settings.API_PREFIX, settings.TOKEN_LOGIN_URL)
    for old_user in old_users:
        subject = render_to_string(
            'apella/emails/old_user_new_credentials_subject.txt'). \
            replace('\n', ' ')
        body = render_to_string(
            'apella/emails/old_user_new_credentials_body.txt',
            {'old_user': old_user, 'login_url': login_url}
        )
        sender = settings.SERVER_EMAIL
        send_mail(
            subject,
            body,
            sender,
            [old_user.email],
            fail_silently=False
        )
