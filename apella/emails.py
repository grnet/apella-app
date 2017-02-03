from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_new_credentials_to_old_users_email(old_users):
    for old_user in old_users:
        subject = render_to_string(
            'apella/emails/old_user_new_credentials_subject.txt'). \
            replace('\n', ' ')
        body = render_to_string(
            'apella/emails/old_user_new_credentials_body.txt',
            {'old_user': old_user, 'baseurl': settings.BASE_URL}
        )
        sender = 'no_reply@grnet.gr'
        send_mail(
            subject,
            body,
            sender,
            [old_user.email],
            fail_silently=False
        )
