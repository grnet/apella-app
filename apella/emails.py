from itertools import chain
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models import Q, Max
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


def send_create_candidacy_emails(candidacy):
    # send to candidate
    send_user_email(
        candidacy.candidate,
        'apella/emails/candidacy_create_subject.txt',
        'apella/emails/candidacy_create_to_candidate_body.txt',
        {'position': candidacy.position})

    # send to managers
    recipients = candidacy.position.department.institution.\
        institutionmanager_set.all().filter(manager_role='institutionmanager')
    for recipient in recipients:
        send_user_email(
            recipient.user,
            'apella/emails/candidacy_create_subject.txt',
            'apella/emails/candidacy_create_to_manager_body.txt',
            {
                'position': candidacy.position,
                'candidate': candidacy.candidate
            })

    # send to secretaries
    recipients = candidacy.position.department.\
        institutionmanager_set.all().filter(is_secretary=True)
    for recipient in recipients:
        send_user_email(
            recipient.user,
            'apella/emails/candidacy_create_subject.txt',
            'apella/emails/candidacy_create_to_manager_body.txt',
            {
                'position': candidacy.position,
                'candidate': candidacy.candidate
            })


def send_remove_candidacy_emails(candidacy):
    # send to candidate
    send_user_email(
        candidacy.candidate,
        'apella/emails/candidacy_remove_subject.txt',
        'apella/emails/candidacy_remove_to_candidate_body.txt',
        {'position': candidacy.position})

    # send to managers
    recipients = candidacy.position.department.institution.\
        institutionmanager_set.all().filter(manager_role='institutionmanager')
    for recipient in recipients:
        send_user_email(
            recipient.user,
            'apella/emails/candidacy_remove_subject.txt',
            'apella/emails/candidacy_remove_to_manager_body.txt',
            {
                'position': candidacy.position,
                'candidate': candidacy.candidate
            })

    # send to secretaries
    recipients = candidacy.position.department.\
        institutionmanager_set.all().filter(is_secretary=True)
    for recipient in recipients:
        send_user_email(
            recipient.user,
            'apella/emails/candidacy_remove_subject.txt',
            'apella/emails/candidacy_remove_to_manager_body.txt',
            {
                'position': candidacy.position,
                'candidate': candidacy.candidate
            })

    # send to electors
    recipients = candidacy.position.electors.all()
    for recipient in recipients:
        send_user_email(
            recipient.user,
            'apella/emails/candidacy_remove_subject.txt',
            'apella/emails/candidacy_remove_to_elector_body.txt',
            {
                'position': candidacy.position,
                'candidate': candidacy.candidate
            })

    # send to committee
    recipients = candidacy.position.committee.all()
    for recipient in recipients:
        send_user_email(
            recipient.user,
            'apella/emails/candidacy_remove_subject.txt',
            'apella/emails/candidacy_remove_to_committee_body.txt',
            {
                'position': candidacy.position,
                'candidate': candidacy.candidate
            })

    # send to cocandidates
    c_set = candidacy.position.candidacy_set.all()
    updated = c_set.values('candidate').annotate(Max('updated_at')).\
        values('updated_at__max')
    candidacies = c_set.filter(Q(updated_at__in=updated) & Q(state='posted'))

    for r in candidacies:
        recipient = r.candidate
        send_user_email(
            recipient,
            'apella/emails/candidacy_remove_subject.txt',
            'apella/emails/candidacy_remove_to_cocandidate_body.txt',
            {
                'position': candidacy.position,
                'candidate': candidacy.candidate
            })


def get_position_users(position):
    recipients = []
    committee = [x.user for x in position.committee.all()]
    electors = [x.user for x in position.electors.all()]
    candidates = [x.candidate for x in position.candidacy_set.all()]
    recipients = chain(committee, candidates, electors)
    return recipients


def send_emails_file(obj, file_kind, extra_context=()):

    position_file_names = ['committee_note', 'committee_proposal',
        'nomination_proceedings', 'nomination_act', 'assistant_files',
        'revocation_decision']

    if file_kind in position_file_names:
        # send to committee, candidates, electors
        subject = 'apella/emails/position_set_{}_subject.txt'.format(file_kind)
        body = 'apella/emails/position_set_{}_body.txt'.format(file_kind)
        recipients = get_position_users(obj)

        for recipient in recipients:
            send_user_email(
                recipient,
                subject,
                body,
                {'position': obj})

    pass


def send_email_elected(obj, elected='elected'):

    if elected == 'elected':
        recipient = obj.elected
    if elected == 'second_best':
        recipient = obj.second_best

    subject = 'apella/emails/position_set_{}_subject.txt'.format(elected)
    body = 'apella/emails/position_set_{}_body.txt'.format(elected)

    # send to elected/second_best
    send_user_email(
        recipient,
        subject,
        body,
        {'position': obj})


def send_emails_field(obj, field, update=False):
    """
    Sends email to appropriate recipients when a field is set or updated
    """

    recipients = []
    context = dict()
    verb = 'set'
    if update:
        verb = 'update'

    position_fields = ['electors_meeting_date',
            'electors_meeting_to_set_committee_date']

    subject = 'apella/emails/position_{}_{}_subject.txt'.format(verb, field)
    body = 'apella/emails/position_{}_{}_body.txt'.format(verb, field)


    if field == 'electors_meeting_to_set_committee_date':
        electors = [x.user for x in obj.electors.all()]
        candidates = [x.candidate for x in obj.candidacy_set.all()]
        recipients = chain(candidates, electors)

    if field == 'electors_meeting_date':
        recipients = get_position_users(obj)

    if field in position_fields:
        context = {'position': obj}


    for recipient in recipients:
        send_user_email(
            recipient,
            subject,
            body,
            context)
