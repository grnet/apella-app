from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from apella.models import InstitutionManager

from apella.util import urljoin


def get_login_url():
    BASE_URL = settings.BASE_URL or '/'
    return urljoin(
        BASE_URL, settings.API_PREFIX, settings.TOKEN_LOGIN_URL)


def send_new_credentials_to_old_users_email(old_users):
    for old_user in old_users:
        subject = render_to_string(
            'apella/emails/old_user_new_credentials_subject.txt'). \
            replace('\n', ' ')
        body = render_to_string(
            'apella/emails/old_user_new_credentials_body.txt',
            {'old_user': old_user, 'login_url': get_login_url()}
        )
        sender = settings.DEFAULT_FROM_EMAIL
        send_mail(
            subject,
            body,
            sender,
            [old_user.email],
            fail_silently=False
        )


def send_user_email(user, template_subject, template_body, extra_context=()):
    subject = render_to_string(template_subject).replace('\n', ' ')
    template_context = {
        'login_url': get_login_url()
    }
    if extra_context:
        template_context.update(extra_context)
    template_context['user'] = user
    body = render_to_string(template_body, template_context)
    sender = settings.DEFAULT_FROM_EMAIL
    send_mail(
        subject,
        body,
        sender,
        [user.email],
        fail_silently=False
    )
    if user.role == 'institutionmanager':
        manager = InstitutionManager.objects.get(user=user)
        if manager:
            template_context['user'] = {
                'first_name': manager.sub_first_name,
                'last_name': manager.sub_last_name,
                'father_name': manager.sub_father_name,
                'email': manager.email,
                'username': ''
            }
            if manager.sub_email:
                body = render_to_string(template_body, template_context)
                send_mail(
                    subject,
                    body,
                    sender,
                    [manager.sub_email],
                    fail_silently=False
                )
