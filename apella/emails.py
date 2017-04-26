import logging
from itertools import chain

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models import Q

from apella.util import urljoin, otz, move_to_timezone
from apella.models import InstitutionManager, UserInterest, \
    ApellaUser

logger = logging.getLogger(__name__)


def get_login_url():
    BASE_URL = settings.BASE_URL or '/'
    return urljoin(
        BASE_URL, settings.API_PREFIX, settings.TOKEN_LOGIN_URL)


def get_ui_url():
    BASE_URL = settings.BASE_URL or '/'
    return urljoin(BASE_URL, settings.UI_PREFIX)


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
    logger.info('%s email sent to %s' % (template_body, str(user.id)))

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
    starts_at = move_to_timezone(candidacy.position.starts_at, otz)
    ends_at = move_to_timezone(candidacy.position.ends_at, otz)
    ui_url = get_ui_url()
    candidacy_url = urljoin(ui_url, 'candidacies/', str(candidacy.pk))
    position_url = urljoin(ui_url, 'positions/', str(candidacy.position.pk))

    # send to candidate
    send_user_email(
        candidacy.candidate,
        'apella/emails/candidacy_create_subject.txt',
        'apella/emails/candidacy_create_to_candidate_body.txt',
        {'position': candidacy.position,
         'starts_at': starts_at,
         'ends_at': ends_at,
         'apella_url': candidacy_url})

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
                'starts_at': starts_at,
                'ends_at': ends_at,
                'candidate': candidacy.candidate,
                'apella_url': position_url
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
                'starts_at': starts_at,
                'ends_at': ends_at,
                'candidate': candidacy.candidate,
                'apella_url': position_url
            })


def send_remove_candidacy_emails(candidacy):
    starts_at = move_to_timezone(candidacy.position.starts_at, otz)
    ends_at = move_to_timezone(candidacy.position.ends_at, otz)
    ui_url = get_ui_url()
    candidacy_url = urljoin(ui_url, 'candidacies/', str(candidacy.pk))
    position_url = urljoin(ui_url, 'positions/', str(candidacy.position.pk))

    # send to candidate
    send_user_email(
        candidacy.candidate,
        'apella/emails/candidacy_remove_subject.txt',
        'apella/emails/candidacy_remove_to_candidate_body.txt',
        {'position': candidacy.position,
         'starts_at': starts_at,
         'ends_at': ends_at,
         'apella_url': candidacy_url})

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
                'starts_at': starts_at,
                'ends_at': ends_at,
                'candidate': candidacy.candidate,
                'apella_url': position_url
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
                'starts_at': starts_at,
                'ends_at': ends_at,
                'candidate': candidacy.candidate,
                'apella_url': position_url
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
                'starts_at': starts_at,
                'ends_at': ends_at,
                'candidate': candidacy.candidate,
                'apella_url': position_url
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
                'starts_at': starts_at,
                'ends_at': ends_at,
                'candidate': candidacy.candidate,
                'apella_url': position_url
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
                'starts_at': starts_at,
                'ends_at': ends_at,
                'candidate': candidacy.candidate,
                'apella_url': position_url
            })


def send_emails_file(obj, file_kind, extra_context=()):

    position_file_names = ['committee_note', 'committee_proposal',
        'nomination_proceedings', 'nomination_act', 'assistant_files',
        'revocation_decision', 'failed_election_decision']

    if file_kind in position_file_names:
        # send to committee, candidates, electors
        subject = 'apella/emails/position_set_{}_subject.txt'.format(file_kind)
        body = 'apella/emails/position_set_{}_body.txt'.format(file_kind)
        recipients = obj.get_users()
        starts_at = move_to_timezone(obj.starts_at, otz)
        ends_at = move_to_timezone(obj.ends_at, otz)
        ui_url = get_ui_url()
        position_url = urljoin(ui_url, 'positions/', str(obj.pk))

        for recipient in recipients:
            send_user_email(
                recipient,
                subject,
                body,
                {'position': obj,
                'starts_at': starts_at,
                'ends_at': ends_at,
                'apella_url': position_url
                })


def send_email_elected(obj, elected='elected'):
    starts_at = move_to_timezone(obj.starts_at, otz)
    ends_at = move_to_timezone(obj.ends_at, otz)

    if elected == 'elected':
        recipient = obj.elected
    if elected == 'second_best':
        recipient = obj.second_best

    subject = 'apella/emails/position_set_{}_subject.txt'.format(elected)
    body = 'apella/emails/position_set_{}_body.txt'.format(elected)
    ui_url = get_ui_url()
    position_url = urljoin(ui_url, 'positions/', str(obj.pk))

    # send to elected/second_best
    send_user_email(
        recipient,
        subject,
        body,
        {'position': obj,
        'starts_at': starts_at,
        'ends_at': ends_at,
        'apella_url': position_url
        })


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
        electors = [x.user for x in obj.electors.filter(is_verified=True).\
            filter(user__is_active=True)]
        candidates = obj.get_candidates_posted()
        recipients = chain(candidates, electors)

    if field == 'electors_meeting_date':
        recipients = obj.get_users()

    if field in position_fields:
        starts_at = move_to_timezone(obj.starts_at, otz)
        ends_at = move_to_timezone(obj.ends_at, otz)
        ui_url = get_ui_url()
        position_url = urljoin(ui_url, 'positions/', str(obj.pk))

        context = {
            'position': obj,
            'starts_at': starts_at,
            'ends_at': ends_at,
            'apella_url': position_url
        }

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
    """
    starts_at = move_to_timezone(position.starts_at, otz)
    ends_at = move_to_timezone(position.ends_at, otz)
    ui_url = get_ui_url()
    position_url = urljoin(ui_url, 'positions/', str(position.pk))
    extra_context = {
        'position': position,
        'starts_at': starts_at,
        'ends_at': ends_at,
        'apella_url': position_url
    }

    if type == 'committee':
        old_c = old_members.get('c', [])
        new_c = new_members.get('c', [])

        if set(old_c) == set(new_c):
            return

        # new committee
        if len(old_c) == 0:
            # send to committee
            recipients = position.committee.filter(is_verified=True).\
                filter(user__is_active=True)
            for recipient in recipients:
                send_user_email(
                    recipient.user,
                    'apella/emails/position_set_committee_subject.txt',
                    'apella/emails/position_set_committee_to_member_body.txt',
                    extra_context)

            # send to electors, candidates
            electors = [x.user for x in position.electors.\
                filter(is_verified=True).\
                filter(user__is_active=True)]

            candidates = position.get_candidates_posted()
            recipients = chain(candidates, electors)

            for recipient in recipients:
                send_user_email(
                    recipient,
                    'apella/emails/position_set_committee_subject.txt',
                    'apella/emails/position_set_committee_body.txt',
                     extra_context)

        else:
            added_committee = [p.user for p in new_c if p not in old_c]
            removed_committee = [p.user for p in old_c if p not in new_c]
            remaining_committee = [
                p.user for p in new_c if p.user not in added_committee]

            # send to electors, candidates, remaining committee
            electors = [x.user for x in position.electors.\
                filter(is_verified=True).\
                filter(user__is_active=True)]
            candidates = position.get_candidates_posted()
            recipients = chain(candidates, electors, remaining_committee)

            if added_committee or removed_committee:
                for recipient in recipients:
                    send_user_email(
                        recipient,
                        'apella/emails/position_update_committee_subject.txt',
                        'apella/emails/position_update_committee_body.txt',
                        extra_context)

                for a in added_committee:
                    send_user_email(
                        a,
                        'apella/emails/position_update_committee_subject.txt',
                        'apella/emails/position_set_committee_to_member_body.txt',
                        extra_context)

                for r in removed_committee:
                    send_user_email(
                        r,
                        'apella/emails/position_update_committee_subject.txt',
                        'apella/emails/position_remove_from_committee_body.txt',
                        extra_context)

    elif type == 'electors':
        old_e = old_members.get('e', [])
        new_e = new_members.get('e', [])

        old_electors_regular = [old_reg.professor for old_reg in
            old_e if old_reg.is_regular]
        old_electors_irregular = [old_irreg.professor for old_irreg in
            old_e if not old_irreg.is_regular]

        new_electors_regular = [new_reg.professor for new_reg in
            new_e if new_reg.is_regular]
        new_electors_irregular = [new_irreg.professor for new_irreg in
            new_e if not new_irreg.is_regular]

        added_regular = [p for p in new_electors_regular
            if p not in old_electors_regular]
        added_irregular = [p for p in new_electors_irregular
            if p not in old_electors_irregular]
        removed_regular = [p for p in old_electors_regular
            if p not in new_electors_regular]
        removed_irregular = [p for p in old_electors_irregular
            if p not in new_electors_irregular]

        candidates = position.get_candidates_posted()
        # new electors set
        if len(old_e) == 0 and len(new_e) > 0:
            for c in candidates:
                send_user_email(
                    c,
                    'apella/emails/position_set_electors_subject.txt',
                    'apella/emails/position_set_electors_body.txt',
                    extra_context)
            for reg in new_electors_regular:
                send_user_email(
                    reg.user,
                    'apella/emails/position_set_electors_subject.txt',
                    'apella/emails/position_set_elector_to_regular_body.txt',
                    extra_context)
            for irreg in new_electors_irregular:
                send_user_email(
                    irreg.user,
                    'apella/emails/position_set_electors_subject.txt',
                    'apella/emails/position_set_elector_to_sub_body.txt',
                    extra_context)

        # update electors set
        elif added_regular or added_irregular \
                or removed_regular or removed_irregular:
            for added_reg in added_regular:
                send_user_email(
                    added_reg.user,
                    'apella/emails/position_set_electors_subject.txt',
                    'apella/emails/position_set_elector_to_regular_body.txt',
                    extra_context)
            for added_irreg in added_irregular:
                send_user_email(
                    added_irreg.user,
                    'apella/emails/position_set_electors_subject.txt',
                    'apella/emails/position_set_elector_to_sub_body.txt',
                    extra_context)
            for removed_reg in removed_regular:
                send_user_email(
                    removed_reg.user,
                    'apella/emails/position_update_electors_subject.txt',
                    'apella/emails/position_remove_elector_to_regular_body.txt',
                    extra_context)
            for removed_irreg in removed_irregular:
                send_user_email(
                    removed_irreg.user,
                    'apella/emails/position_update_electors_subject.txt',
                    'apella/emails/position_remove_elector_to_sub_body.txt',
                    extra_context)



            # send to electors, candidates
            electors = [p.user for p in position.electors.\
                filter(is_verified=True).\
                filter(user__is_active=True)
                if p not in added_irregular and p not in removed_irregular
                and p not in added_regular and p not in removed_regular]
            committee = [p.user for p in position.committee.\
                filter(is_verified=True).\
                filter(user__is_active=True)]
            recipients = chain(electors, committee, candidates)

            for user in recipients:
                send_user_email(
                    user,
                    'apella/emails/position_update_electors_subject.txt',
                    'apella/emails/position_update_electors_body.txt',
                    extra_context)


def send_position_create_emails(position):
    starts_at = move_to_timezone(position.starts_at, otz)
    ends_at = move_to_timezone(position.ends_at, otz)
    ui_url = get_ui_url()
    position_url = urljoin(ui_url, 'positions/', str(position.pk))
    extra_context = {
        'position': position,
        'starts_at': starts_at,
        'ends_at': ends_at,
        'apella_url': position_url
    }

    send_user_email(
        position.author.user,
        'apella/emails/position_create_subject.txt',
        'apella/emails/position_create_to_manager.txt',
        extra_context)

    if position.is_election_type:
        users_interested = UserInterest.objects.filter(
            Q(area=position.subject_area) |
            Q(subject=position.subject) |
            Q(institution=position.department.institution) |
            Q(department=position.department)). \
            values_list('user', flat=True).distinct()
        users_to_email = ApellaUser.objects.filter(is_active=True).filter(
            Q(professor__is_verified=True) |
            Q(candidate__is_verified=True)).filter(id__in=users_interested)

        for user in users_to_email:
            send_user_email(
                user,
                'apella/emails/position_create_subject.txt',
                'apella/emails/position_create_to_interested.txt',
                extra_context)
    elif position.user_application:
        user = position.user_application.user
        extra_context['user_application'] = position.user_application
        send_user_email(
            user,
            'apella/emails/position_create_subject.txt',
            'apella/emails/position_create_to_professor.txt',
            extra_context)

def send_create_application_emails(user_application):
    managers = InstitutionManager.objects.filter(
        institution=user_application.user.professor.department.institution)
    for manager in managers:
        send_user_email(
            manager.user,
            'apella/emails/user_application_create_subject.txt',
            'apella/emails/user_application_create_body.txt')

    send_user_email(
        user_application.user,
        'apella/emails/user_application_create_subject.txt',
        'apella/emails/user_application_create_body.txt')
