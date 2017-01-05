import logging
import re
from django.db import transaction

from apella.models import ApellaUser, MultiLangFields, Candidate, \
    Institution, Department, Professor, InstitutionManager, \
    OldApellaUserMigrationData

logger = logging.getLogger('apella')


def get_institution(institution_id_str):
    if not institution_id_str:
        return None
    try:
        institution_id = int(institution_id_str)
        institution = Institution.objects.get(id=institution_id)
    except ValueError:
        logger.error('invalid institution id %s' % institution_id_str)
        raise
    except TypeError:
        logger.error('invalid institution id %s' % institution_id_str)
        raise
    except Institution.DoesNotExist:
        logger.error('institution %s does not exist' % institution_id_str)
        raise
    logger.info('got institution %s' % institution.id)
    return institution


def get_department(department_id_str):
    if not department_id_str:
        return None
    try:
        department_id = int(department_id_str)
        department = Department.objects.get(id=department_id)
    except ValueError:
        logger.error('invalid department id %s' % department_id_str)
        raise
    except Department.DoesNotExist:
        logger.error('department %s does not exist' % department_id_str)
        raise
    logger.info('got department %s' % department.id)
    return department


def migrate_candidate(old_user, new_user):
    candidate = Candidate.objects.create(user=new_user)
    return candidate


def migrate_professor(old_user, new_user):
    institution = get_institution(old_user.professor_institution_id)
    department = get_department(old_user.professor_department_id)

    discipline_in_fek = False
    discipline_text = None
    if old_user.professor_subject_from_appointment:
        discipline_in_fek = True
        discipline_text = old_user.professor_subject_from_appointment
    else:
        discipline_text = old_user.professor_subject_optional_freetext

    professor = Professor.objects.create(
        user=new_user,
        institution=institution,
        department=department,
        rank=old_user.professor_rank,
        is_foreign=bool(re.match('t', old_user.is_foreign, re.I)),
        speaks_greek=bool(re.match('t', old_user.speaks_greek, re.I)),
        cv_url=old_user.professor_institution_cv_url,
        fek=old_user.professor_appointment_gazette_url,
        discipline_in_fek=discipline_in_fek,
        discipline_text=discipline_text)

    return professor


def migrate_institutionmanager(old_user, new_user):
    institution = get_institution(old_user.manager_institution_id)

    sub_first_name = MultiLangFields.objects.create(
        el=old_user.manager_deputy_name_el,
        en=old_user.manager_deputy_name_en)
    sub_last_name = MultiLangFields.objects.create(
        el=old_user.manager_deputy_surname_el,
        en=old_user.manager_deputy_surname_en)
    sub_father_name = MultiLangFields.objects.create(
        el=old_user.manager_deputy_fathername_el,
        en=old_user.manager_deputy_fathername_en)

    try:
        manager = InstitutionManager.objects.create(
            user=new_user,
            institution=institution,
            authority=old_user.manager_appointer_authority,
            authority_full_name=old_user.manager_appointer_fullname,
            manager_role=new_user.role,
            sub_first_name=sub_first_name,
            sub_last_name=sub_last_name,
            sub_father_name=sub_father_name,
            sub_mobile_phone_number=old_user.manager_deputy_mobile,
            sub_home_phone_number=old_user.manager_deputy_phone,
            sub_email=old_user.manager_deputy_email)
    except ValueError as e:
        logger.error('failed to migrate user %s' % old_user.user_id)
        logger.error(e)
        raise

    return manager


def professor_exists(user_id):
    return OldApellaUserMigrationData.objects.filter(
        role='professor', user_id=user_id).exists()


@transaction.atomic
def migrate_user(old_user):

    if ApellaUser.objects.filter(username=old_user.username).exists():
        if (not professor_exists(old_user.user_id) and
                old_user.role == 'candidate') or old_user.role != 'candidate':
            logger.error(
                'a user with username %s already exists, user_id: %s' %
                (old_user.username, old_user.user_id))
        return
    if ApellaUser.objects.filter(email=old_user.email).exists():
        if (not professor_exists(old_user.user_id) and
                old_user.role == 'candidate') or old_user.role != 'candidate':
            logger.error(
                'a user with email %s already exists, user_id: %s' %
                (old_user.email, old_user.user_id))
        return

    first_name = MultiLangFields.objects.create(
        el=old_user.name_el,
        en=old_user.name_en)
    last_name = MultiLangFields.objects.create(
        el=old_user.surname_el,
        en=old_user.surname_en)
    father_name = MultiLangFields.objects.create(
        el=old_user.fathername_el,
        en=old_user.fathername_en)

    if not old_user.username or old_user.username == '':
        username = 'user' + old_user.user_id
    else:
        username = old_user.username

    new_user = ApellaUser.objects.create(
        username=username,
        role=old_user.role,
        first_name=first_name,
        last_name=last_name,
        father_name=father_name,
        email=old_user.email,
        id_passport=old_user.person_id_number,
        mobile_phone_number=old_user.mobile,
        home_phone_number=old_user.phone,
        is_active=True)
    logger.info(
        'created user %s, user_id %s' % (new_user.id, old_user.user_id))

    role = old_user.role
    if role == 'candidate':
        if not professor_exists(old_user.user_id):
            candidate = migrate_candidate(old_user, new_user)
            logger.info('created candidate %s' % candidate.id)
    elif role == 'professor':
        professor = migrate_professor(old_user, new_user)
        logger.info('created professor %s' % professor.id)
    elif role == 'institutionmanager' or role == 'assistant':
        institutionmanager = migrate_institutionmanager(old_user, new_user)
        logger.info('created institution manager %s' % institutionmanager.id)

    return new_user
