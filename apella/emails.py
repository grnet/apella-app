from itertools import chain

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
    pos = candidacy.position
    recipients = pos.get_candidates_posted()
    for recipient in recipients:
        send_user_email(
            recipient,
            'apella/emails/candidacy_remove_subject.txt',
            'apella/emails/candidacy_remove_to_cocandidate_body.txt',
            {
                'position': candidacy.position,
                'candidate': candidacy.candidate
            })



def send_emails_file(obj, file_kind, extra_context=()):

    position_file_names = ['committee_note', 'committee_proposal',
        'nomination_proceedings', 'nomination_act', 'assistant_files',
        'revocation_decision']

    if file_kind in position_file_names:
        # send to committee, candidates, electors
        subject = 'apella/emails/position_set_{}_subject.txt'.format(file_kind)
        body = 'apella/emails/position_set_{}_body.txt'.format(file_kind)
        recipients = obj.get_users()

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
        candidates = obj.get_candidates_posted()
        recipients = chain(candidates, electors)

    if field == 'electors_meeting_date':
        recipients = obj.get_users()

    if field in position_fields:
        context = {'position': obj}

    for recipient in recipients:
        send_user_email(
            recipient,
            subject,
            body,
            context)


def send_emails_members_change(position, type, old_members, new_members):
    """
    Sends emails to appropriate recipients when members of committee or
    electors are set or updated

    Args:
        position: Position object
        type(str): Members type ('committee' or 'electors')
        old_members(dict): Members before the update
        new_members(dict): Members after the update

    {old, new}_members for committee are expected to be in the format:
    {
        c: committee,
    }
    {old, new}_members for electors are expected to be in the format:
    {
        e_r_e: electors_regular_external,
        e_r_i: electors_regular_internal,
        e_s_e: electors_sub_external,
        e_s_i: electors_sub_internal,
    }
    """
    if type == 'committee':
        old_c = old_members.get('c', [])
        new_c = new_members.get('c', [])

        if set(old_c) == set(new_c):
            return

        # new committee
        if len(old_c) == 0:
            # send to committee
            recipients = position.committee.all()
            for recipient in recipients:
                send_user_email(
                    recipient.user,
                    'apella/emails/position_set_committee_subject.txt',
                    'apella/emails/position_set_committee_to_member_body.txt',
                    {'position': position})

            # send to electors, candidates
            electors = [x.user for x in position.electors.all()]
            candidates = position.get_candidates_posted()
            recipients = chain(candidates, electors)

            for recipient in recipients:
                send_user_email(
                    recipient,
                    'apella/emails/position_set_committee_subject.txt',
                    'apella/emails/position_set_committee_body.txt',
                    {'position': position})

        else:
            added_committee = list(set(new_c) - set(old_c))
            removed_committee = list(set(new_c) - set(old_c))
            remaining_committee = list(set(new_c).intersection(set(old_c)))

            # send to electors, candidates, remaining committee
            electors = [x.user for x in position.electors.all()]
            committee = [x.user for x in remaining_committee]
            candidates = position.get_candidates_posted()
            recipients = chain(candidates, electors, committee)

            for recipient in recipients:
                print recipient.first_name.el
                send_user_email(
                    recipient,
                    'apella/emails/position_update_committee_subject.txt',
                    'apella/emails/position_update_committee_body.txt',
                    {'position': position})

            for a in added_committee:
                print a.user.first_name.el
                send_user_email(
                    a.user,
                    'apella/emails/position_update_committee_subject.txt',
                    'apella/emails/position_set_committee_to_member_body.txt',
                    {'position': position})

            for r in removed_committee:
                print r.user.first_name.el
                send_user_email(
                    r.user,
                    'apella/emails/position_update_committee_subject.txt',
                    'apella/emails/position_remove_from_committee_body.txt',
                    {'position': position})
