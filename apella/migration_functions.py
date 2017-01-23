import logging
import re
import os
from datetime import datetime

from django.db import transaction, DataError
from django.conf import settings
from django.db.utils import IntegrityError
from django.core.files import File

from apella.models import ApellaUser, MultiLangFields, Candidate, \
    Institution, Department, Professor, InstitutionManager, \
    OldApellaUserMigrationData, Position, Subject, SubjectArea, \
    OldApellaPositionMigrationData, ApellaFile, OldApellaFileMigrationData, \
    Candidacy, OldApellaCandidacyMigrationData, \
    OldApellaCandidacyFileMigrationData, OldApellaInstitutionMigrationData

from apella.common import FILE_KIND_TO_FIELD, AUTHORITIES

logger = logging.getLogger('apella')


def get_obj(id_str, model):
    if not id_str:
        return None
    try:
        id = int(id_str)
        obj = model.objects.get(id=id)
    except ValueError:
        logger.error('invalid id %s' % id_str)
        raise
    except TypeError:
        logger.error('invalid id %s' % id_str)
        raise
    except model.DoesNotExist:
        logger.error('%s %s does not exist' % (model.__name__, id_str))
        raise
    logger.debug('got %s %s' % (model.__name__, id))
    return obj


def migrate_candidate(old_user, new_user):
    is_verified = True if old_user.role_status == 'ACTIVE' else False
    candidate = Candidate.objects.create(
        user=new_user,
        is_verified=is_verified)
    return candidate


@transaction.atomic
def migrate_professor(old_user, new_user):
    institution = get_obj(old_user.professor_institution_id, Institution)
    department = get_obj(old_user.professor_department_id, Department)

    discipline_in_fek = False
    discipline_text = None
    if bool(re.match('t', old_user.professor_subject_from_appointment, re.I)):
        discipline_in_fek = True
        discipline_text = old_user.professor_subject_from_appointment
    else:
        discipline_text = old_user.professor_subject_optional_freetext

    is_verified = True if old_user.role_status == 'ACTIVE' else False

    professor = Professor.objects.create(
        user=new_user,
        institution=institution,
        institution_freetext=old_user.professor_institution_freetext,
        department=department,
        rank=old_user.professor_rank,
        is_foreign=bool(re.match('t', old_user.is_foreign, re.I)),
        speaks_greek=bool(re.match('t', old_user.speaks_greek, re.I)),
        cv_url=old_user.professor_institution_cv_url,
        fek=old_user.professor_appointment_gazette_url,
        discipline_in_fek=discipline_in_fek,
        discipline_text=discipline_text,
        is_verified=is_verified)

    return professor


@transaction.atomic
def migrate_institutionmanager(old_user, new_user):
    institution = get_obj(old_user.manager_institution_id, Institution)

    sub_first_name = MultiLangFields.objects.create(
        el=old_user.manager_deputy_name_el,
        en=old_user.manager_deputy_name_en)
    sub_last_name = MultiLangFields.objects.create(
        el=old_user.manager_deputy_surname_el,
        en=old_user.manager_deputy_surname_en)
    sub_father_name = MultiLangFields.objects.create(
        el=old_user.manager_deputy_fathername_el,
        en=old_user.manager_deputy_fathername_en)

    if old_user.manager_appointer_authority:
        authority = [
            authority for authority, value in AUTHORITIES
            if authority == old_user.manager_appointer_authority.lower()][0]
    else:
        authority = None

    try:
        manager = InstitutionManager.objects.create(
            user=new_user,
            institution=institution,
            authority=authority,
            authority_full_name=old_user.manager_appointer_fullname,
            manager_role=new_user.role,
            sub_first_name=sub_first_name,
            sub_last_name=sub_last_name,
            sub_father_name=sub_father_name,
            sub_mobile_phone_number=old_user.manager_deputy_mobile,
            sub_home_phone_number=old_user.manager_deputy_phone,
            sub_email=old_user.manager_deputy_email,
            is_verified=True)
    except ValueError as e:
        logger.error('failed to migrate user %s' % old_user.user_id)
        logger.error(e)
        raise

    return manager


def professor_exists(user_id):
    return OldApellaUserMigrationData.objects.filter(
        role='professor', user_id=user_id).exists()

FILE_KINDS_MAPPING = {
    'profile': {
        'BIOGRAFIKO': 'cv',
        'PTYXIO': 'diploma',
        'DIMOSIEYSI': 'publication',
        'TAYTOTHTA': 'id_passport',
        'PROFILE': 'cv_professor'
    },
    'candidacy': {
        'BIOGRAFIKO': 'cv',
        'PTYXIO': 'diploma',
        'DIMOSIEYSI': 'publication',
        'EKTHESI_AUTOAKSIOLOGISIS': 'self_evaluation_report',
        'SYMPLIROMATIKA_EGGRAFA': 'attachment_files'
    }
}


@transaction.atomic
def migrate_file(old_file, new_user, source, source_id):
    if old_file.file_type not in FILE_KINDS_MAPPING[source]:
        logger.error(
            'failed to migrate file, unknown file_type %s for %s' %
            (old_file.file_type, source))
        return
    new_file = ApellaFile(
        owner=new_user,
        description=old_file.file_description,
        file_kind=FILE_KINDS_MAPPING[source][old_file.file_type],
        source=source,
        source_id=source_id)
    old_file_path = os.path.join(
        settings.OLD_APELLA_MEDIA_ROOT, old_file.file_path)
    try:
        with open(old_file_path, 'r') as f:
            new_file.file_path.save(
                old_file.original_name, File(f))
            new_file.file_path.file.close()
    except IOError:
        logger.error('failed to migrate file %s' % old_file.file_path)
        return
    logger.info(
        'migrated %s file %s to %s' %
        (source, old_file.id, new_file.id))

    field_name, many = \
        FILE_KIND_TO_FIELD[FILE_KINDS_MAPPING[source][old_file.file_type]].values()
    if source == 'profile':
        if new_user.is_professor():
            if not many:
                setattr(new_user.professor, field_name, new_file)
            else:
                many_attr = getattr(new_user.professor, field_name)
                many_attr.add(new_file)
            new_user.professor.save()
        elif new_user.is_candidate():
            if not many:
                setattr(new_user.candidate, field_name, new_file)
            else:
                many_attr = getattr(new_user.candidate, field_name)
                many_attr.add(new_file)
            new_user.candidate.save()
    elif source == 'candidacy':
        candidacy = Candidacy.objects.get(id=source_id)
        if not many:
            setattr(candidacy, field_name, new_file)
        else:
            many_attr = getattr(candidacy, field_name)
            many_attr.add(new_file)
        candidacy.save()

@transaction.atomic
def migrate_user_profile_files(old_user, new_user):
    old_files = OldApellaFileMigrationData.objects.filter(
        user_id=old_user.user_id)
    i = 0
    for old_file in old_files:
        migrate_file(
            old_file, new_user, 'profile', new_user.id)
        i += 1
    logger.info(
        'migrated %s profile files for user %s' %
        (i, new_user.id))


@transaction.atomic
def migrate_username(username, password=None):
    old_users = OldApellaUserMigrationData.objects.filter(username=username)
    for old_user in old_users:
        if professor_exists(old_user.user_id) and old_user.role == 'candidate':
            continue
        new_user = migrate_user(old_user, password)
        if new_user:
            return new_user


@transaction.atomic
def migrate_shibboleth_id(shibboleth_id):
    old_users = OldApellaUserMigrationData.objects.filter(
        shibboleth_id=shibboleth_id)
    for old_user in old_users:
        if professor_exists(old_user.user_id) and old_user.role == 'candidate':
            continue
        new_user = migrate_user(old_user)
        if new_user:
            return new_user


@transaction.atomic
def migrate_user(old_user, password=None):
    if ApellaUser.objects.filter(username=old_user.username).exists():
        logger.error(
            'a user with username %s already exists, user_id: %s' %
            (old_user.username, old_user.user_id))
        return
    if ApellaUser.objects.filter(email=old_user.email).exists():
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
        is_active=True,
        email_verified=True,
        old_user_id=int(old_user.user_id))

    if password:
        new_user.set_password(password)
        new_user.save()
    else:
        new_user.set_unusable_password()

    logger.info(
        'created user %s from user_id %s' % (new_user.id, old_user.user_id))

    role = old_user.role
    if role == 'candidate':
        if not professor_exists(old_user.user_id):
            candidate = migrate_candidate(old_user, new_user)
            logger.info('created candidate %s' % candidate.id)
            migrate_user_profile_files(old_user, new_user)
            migrate_candidacies(candidate_user=new_user)
    elif role == 'professor':
        professor = migrate_professor(old_user, new_user)
        logger.info('created professor %s' % professor.id)
        migrate_user_profile_files(old_user, new_user)
        migrate_candidacies(candidate_user=new_user)
    elif role == 'institutionmanager' or role == 'assistant':
        institutionmanager = migrate_institutionmanager(old_user, new_user)
        logger.info('created institution manager %s' % institutionmanager.id)
        department_ids = Department.objects.filter(
            institution=institutionmanager.institution).values_list(
                'id', flat=True)
        if role == 'institutionmanager':
            old_positions = OldApellaPositionMigrationData.objects.filter(
                department_id__in=map(str, department_ids))
            for old_position in old_positions:
                migrate_position(old_position, institutionmanager)

    return new_user


@transaction.atomic
def migrate_position(old_position, author):
    if Position.objects.filter(old_code=old_position.position_serial). \
            exists():
        logger.info('position %s already exists' % old_position.position_serial)
        return

    subject = get_obj(old_position.subject_code, Subject)
    subject_area = get_obj(old_position.subject_area_code, SubjectArea)
    department = get_obj(old_position.department_id, Department)
    fek_posted_at = datetime.strptime(
        old_position.gazette_publication_date, '%Y-%m-%d')
    starts_at = datetime.strptime(
        old_position.opening_date, '%Y-%m-%d')
    ends_at = datetime.strptime(
        old_position.closing_date, '%Y-%m-%d')

    try:
        new_position = Position.objects.create(
            old_code=old_position.position_serial,
            title=old_position.title,
            description=old_position.description,
            subject=subject,
            subject_area=subject_area,
            author=author,
            discipline=old_position.subject_id,
            department=department,
            department_dep_number=0,
            fek=old_position.gazette_publication_url,
            fek_posted_at=fek_posted_at,
            state='posted',
            starts_at=starts_at,
            ends_at=ends_at
        )
    except IntegrityError as e:
        logger.error(
            'failed to migrate position %s' % old_position.position_serial)
        logger.error(e)
        return
    except DataError as e:
        logger.error(
            'failed to migrate position %s' % old_position.position_serial)
        logger.error(e)
        return

    new_position.code = settings.POSITION_CODE_PREFIX + str(new_position.id)
    new_position.save()

    logger.info(
        'migrated position %s, from old position %s' %
        (new_position.id, old_position.position_serial))

    migrate_candidacies(position=new_position)
    return new_position


@transaction.atomic
def migrate_candidacies(position=None, candidate_user=None):
    if position:
        old_candidacies = OldApellaCandidacyMigrationData.objects.filter(
            position_serial=str(position.old_code))
    elif candidate_user:
        old_candidacies = OldApellaCandidacyMigrationData.objects.filter(
            candidate_user_id=str(candidate_user.old_user_id))
        for old_candidacy in old_candidacies:
            if Candidacy.objects.filter(
                    old_candidacy_id=int(old_candidacy.candidacy_serial)).exists():
                logger.info(
                    'already migrated candidacy %s' %
                    old_candidacy.candidacy_serial)
                continue
            try:
                new_candidate = ApellaUser.objects.get(
                    old_user_id=int(old_candidacy.candidate_user_id))
            except ApellaUser.DoesNotExist:
                logger.info(
                    'cannot migrate candidacy %s: candidate %s does not exist'
                    % (old_candidacy.candidacy_serial,
                        old_candidacy.candidate_user_id))
                continue

            try:
                new_position = Position.objects.get(
                    old_code=old_candidacy.position_serial)
            except Position.DoesNotExist:
                logger.info(
                    'cannot migrate candidacy %s: position %s does not exist' %
                    (old_candidacy.candidacy_serial,
                        old_candidacy.position_serial))
                continue

            migrate_candidacy(old_candidacy, new_candidate, new_position)


@transaction.atomic
def migrate_candidacy_files(new_candidacy):
    old_candidacy_files = OldApellaCandidacyFileMigrationData. \
        objects.filter(candidacy_serial=str(new_candidacy.old_candidacy_id))
    for old_file in old_candidacy_files:
        migrate_file(
            old_file, new_candidacy.candidate, 'candidacy', new_candidacy.id)

@transaction.atomic
def migrate_candidacy(old_candidacy, new_candidate, new_position):
    candidacy = Candidacy.objects.create(
        candidate=new_candidate,
        position=new_position,
        state='posted',
        others_can_view=bool(
            re.match('t', old_candidacy.open_to_other_candidates, re.I)),
        old_candidacy_id=int(old_candidacy.candidacy_serial))

    candidacy.code = str(candidacy.id)
    candidacy.save()
    logger.info(
        'migrated candidacy %s, to %s' %
        (old_candidacy.candidacy_serial, candidacy.id))

    migrate_candidacy_files(candidacy)

def migrate_institutions_metadata():
    for old_institution in OldApellaInstitutionMigrationData.objects.all():
        try:
            new_institution = Institution.objects.get(
                id=old_institution.institution_id)
        except Institution.DoesNotExist:
            logger.error(
                'could not migrate institution\'s metadata:'
                'institution %s dooes not exist' %
                old_institution.institution_id)
            continue
        new_institution.organization = \
            old_institution.institution_organization_url
        new_institution.regulatory_framework = \
            old_institution.institution_bylaw_url
        new_institution.save()
