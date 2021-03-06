import logging
import re
import os
import errno
from datetime import datetime

from django.db import transaction, DataError
from django.conf import settings
from django.db.utils import IntegrityError
from django.db.models import Min
from django.core.exceptions import MultipleObjectsReturned

from apella.models import ApellaUser, MultiLangFields, Candidate, \
    Institution, Department, Professor, InstitutionManager, \
    OldApellaUserMigrationData, Position, Subject, SubjectArea, \
    OldApellaPositionMigrationData, ApellaFile, OldApellaFileMigrationData, \
    Candidacy, OldApellaCandidacyMigrationData, \
    OldApellaCandidacyFileMigrationData, OldApellaInstitutionMigrationData, \
    OldApellaCandidateAssistantProfessorMigrationData, generate_filename, \
    OldApellaAreaSubscriptions, UserInterest

from apella.common import FILE_KIND_TO_FIELD, AUTHORITIES

from apella.util import safe_path_join, otz, at_day_start, \
    at_day_end, strip_timezone, timezone
from apella.serials import get_serial

eet = timezone('EET')

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
    try:
        candidate = new_user.candidate
        candidate.is_verified = is_verified
        candidate.save()
    except Candidate.DoesNotExist:
        candidate = Candidate.objects.create(
            user=new_user,
            is_verified=is_verified)
        logger.info('created candidate %s' % candidate.id)
    return candidate


@transaction.atomic
def migrate_professor(old_user, new_user):
    institution = get_obj(old_user.professor_institution_id, Institution)
    department = get_obj(old_user.professor_department_id, Department)

    discipline_in_fek = False
    discipline_text = None
    if old_user.professor_subject_from_appointment:
        discipline_in_fek = True
        discipline_text = old_user.professor_subject_from_appointment
    else:
        discipline_text = old_user.professor_subject_optional_freetext
    is_verified = True if old_user.role_status == 'ACTIVE' else False

    try:
        professor = new_user.professor
        professor.institution = institution
        professor.institution_freetext = \
            old_user.professor_institution_freetext
        professor.department = department
        professor.rank = old_user.professor_rank
        professor.is_foreign = bool(re.match('t', old_user.is_foreign, re.I))
        professor.speaks_greek = bool(re.match('t', old_user.speaks_greek, re.I))
        professor.cv_url = old_user.professor_institution_cv_url
        professor.fek = old_user.professor_appointment_gazette_url
        professor.discipline_in_fek = discipline_in_fek
        professor.discipline_text = discipline_text
        professor.is_verified = is_verified
        professor.save()

    except Professor.DoesNotExist:

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
        logger.info('created professor %s' % professor.id)

    if institution and institution.has_shibboleth and not new_user.shibboleth_id:
        new_user.can_set_academic = True
    else:
        new_user.can_set_academic = False
    new_user.save()
    return professor


@transaction.atomic
def migrate_institutionmanager(old_user, new_user):
    institution = get_obj(old_user.manager_institution_id, Institution)
    if old_user.manager_appointer_authority:
        authority = [
            authority for authority, value in AUTHORITIES
            if authority == old_user.manager_appointer_authority.lower()][0]
    else:
        authority = None

    try:
        manager = new_user.institutionmanager
        manager.institution = institution
        manager.authority = authority
        manager.authority_full_name = old_user.manager_appointer_fullname
        manager.manager_role = new_user.role
        manager.sub_first_name.el = old_user.manager_deputy_name_el
        manager.sub_first_name.en = old_user.manager_deputy_name_en
        manager.sub_first_name.save()
        manager.sub_last_name.el = old_user.manager_deputy_surname_el
        manager.sub_last_name.en = old_user.manager_deputy_surname_en
        manager.sub_last_name.save()
        manager.sub_father_name.el = old_user.manager_deputy_fathername_el
        manager.sub_father_name.en = old_user.manager_deputy_fathername_en
        manager.sub_father_name.save()
        manager.sub_mobile_phone_number = old_user.manager_deputy_mobile
        manager.sub_home_phone_number = old_user.manager_deputy_phone
        manager.sub_email = old_user.manager_deputy_email
        manager.save()

    except InstitutionManager.DoesNotExist:

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
            logger.info(
                'created institution manager %s' % manager.id)
        except ValueError as e:
            logger.error('failed to migrate user %s' % old_user.user_id)
            logger.error(e)
            raise

    return manager


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


def set_attr_files(obj, field_name, many, new_file):
    if not many:
        setattr(obj, field_name, new_file)
    else:
        many_attr = getattr(obj, field_name)
        many_attr.add(new_file)
    obj.save()


def remove_attr_files(obj):
    obj.cv = None
    obj.diplomas.all().delete()
    obj.publications.all().delete()

    if isinstance(obj, Candidacy):
        obj.self_evaluation_report = None
        obj.attachment_files.all().delete()
    if isinstance(obj, Professor):
        obj.cv_professor = None
    if isinstance(obj, Candidate):
        obj.id_passport_file = None

    obj.save()


@transaction.atomic
def migrate_file(old_file, new_user, source, source_id):

    if old_file.file_type not in FILE_KINDS_MAPPING[source]:
        return

    updated_at = strip_timezone(old_file.updated_at.replace(tzinfo=eet)) \
        if old_file.updated_at else datetime.utcnow()
    new_file = ApellaFile(
        id=get_serial('apella_file'),
        owner=new_user,
        description=old_file.file_description,
        file_kind=FILE_KINDS_MAPPING[source][old_file.file_type],
        source=source,
        source_id=source_id,
        updated_at=updated_at,
        file_name=old_file.original_name)
    new_file_path = safe_path_join(
        settings.MEDIA_ROOT,
        generate_filename(new_file, old_file.original_name))
    new_file.file_content = new_file_path
    new_file.old_file_path = old_file.file_path
    new_file.save()

    field_name, many = \
        FILE_KIND_TO_FIELD[FILE_KINDS_MAPPING[source][old_file.file_type]].\
        values()
    if source == 'profile':
        if new_user.is_professor():
            set_attr_files(new_user.professor, field_name, many, new_file)
        elif new_user.is_candidate():
            set_attr_files(new_user.candidate, field_name, many, new_file)
    elif source == 'candidacy':
        candidacy = Candidacy.objects.get(id=source_id)
        set_attr_files(candidacy, field_name, many, new_file)


def link_migrated_files(apellafiles):
    path_join = os.path.join
    old_root = settings.OLD_APELLA_MEDIA_ROOT
    new_root = settings.MEDIA_ROOT
    nr_files = 0
    missing_files = 0
    error_files = 0

    for apellafile in apellafiles:
        nr_files += 1
        if nr_files & 1023 == 0:
            m = "files so far: %d, missing: %d, errors: %d"
            m %= (nr_files, missing_files, error_files)
            logger.info(m)

        old_file_path = apellafile.old_file_path
        if not old_file_path:
            continue

        old_full_path = path_join(old_root, old_file_path)
        new_full_path = path_join(new_root, apellafile.file_content.path)

        retry = 1
        while retry >= 0:
            try:
                os.link(old_full_path, new_full_path)
                missing_files += 1
                break

            except OSError as e:
                pass

            if e.errno == errno.EEXIST:
                break

            elif e.errno == errno.ENOENT:
                if not os.path.exists(old_full_path):
                    m = "Cannot link %r to %r: source is missing"
                    m = m % (old_full_path, new_full_path)
                    logger.error(m)
                    error_files += 1
                    break

                try:
                    os.makedirs(os.path.dirname(new_full_path))
                except OSError as ee:
                    m = "Cannot link %r to %r: makedirs failed: %s"
                    m = m % (old_full_path, new_full_path, ee)
                    logger.error(m)
                    error_files += 1
                    break

            else:
                m = "Cannot link %r to %r: %s"
                m = m % (old_full_path, new_full_path, e)
                logger.error(m)
                error_files += 1
                break

            retry -= 1

    m = "total files: %d, missing: %d, errors: %d"
    m %= (nr_files, missing_files, error_files)
    logger.info(m)
    return nr_files, missing_files, error_files


@transaction.atomic
def migrate_user_profile_files(old_user, new_user):
    old_files = OldApellaFileMigrationData.objects.filter(
        user_id=old_user.user_id)

    if new_user.is_professor():
        remove_attr_files(new_user.professor)
    elif new_user.is_candidate():
        remove_attr_files(new_user.candidate)

    for old_file in old_files:
        migrate_file(old_file, new_user, 'profile', new_user.id)


def get_old_users_by_username(username):
    return OldApellaUserMigrationData.objects.filter(username=username)


def get_old_users_by_shibboleth_id(shibboleth_id):
    return OldApellaUserMigrationData.objects.filter(shibboleth_id=shibboleth_id)


@transaction.atomic
def migrate_username(username, password=None, login=False):
    old_users = get_old_users_by_username(username)
    roles = {}
    for old_user in old_users:
        roles[old_user.role] = old_user

    if 'professor' in roles:
        return migrate_user(roles['professor'], password=password, login=login)

    if 'candidate' in roles:
        return migrate_user(roles['candidate'], password=password, login=login)

    roles.pop('assistant', None)
    if len(roles) > 1:
        m = "username: %r" % username
        raise AssertionError(m)

    for role, old_user in roles.iteritems():
        return migrate_user(old_user, password=password, login=login)


@transaction.atomic
def migrate_shibboleth_id(apella2_shibboleth_id,
                          old_apella_shibboleth_id,
                          migration_key=None,
                          login=False):

    old_users = get_old_users_by_shibboleth_id(old_apella_shibboleth_id)

    if migration_key is not None:
        unfiltered_old_users = old_users
        old_users = [x for x in old_users if x.migration_key == migration_key]
        if not old_users:
            m = "could not match migration key for old %r / new %r, %r vs %r"
            m %= (old_apella_shibboleth_id, apella2_shibboleth_id,
                  migration_key,
                  [x.migration_key for x in unfiltered_old_users])
            logger.info(m)

    roles = {}
    for old_user in old_users:
        roles[old_user.role] = old_user

    if 'professor' in roles and 'candidate' in roles:
        old_candidate = roles.pop('candidate')
        old_candidate.migration_key = None
        old_candidate.save()

    if len(roles) > 1:
        m = "old_apella_shibboleth_id: %r" % old_apella_shibboleth_id
        raise AssertionError(m)

    for role, old_user in roles.iteritems():
        return migrate_user(old_user,
                            apella2_shibboleth_id=apella2_shibboleth_id,
                            login=login)


@transaction.atomic
def migrate_user(
    old_user, password=None, apella2_shibboleth_id=None, login=False):

    new_user = create_or_update_user(
        old_user, password=password,
        apella2_shibboleth_id=apella2_shibboleth_id)

    if new_user is None:
        return None

    new_user.save()
    migrate_user_role(old_user, new_user, login=login)

    old_user.migrated_at = datetime.utcnow()
    old_user.save()

    return new_user


def create_or_update_user(
        old_user, password=None, apella2_shibboleth_id=None):

    if not old_user.email:
        return None

    if not old_user.name_el:
        old_user.name_el = old_user.name_en
    if not old_user.name_en:
        old_user.name_en = old_user.name_el
    if not old_user.surname_el:
        old_user.surname_el = old_user.surname_en
    if not old_user.surname_en:
        old_user.surname_en = old_user.surname_el
    if not old_user.fathername_el:
        old_user.fathername_el = old_user.fathername_en
    if not old_user.fathername_en:
        old_user.fathername_en = old_user.fathername_el

    try:
        new_user = ApellaUser.objects.get(old_user_id=old_user.user_id)
        new_user.first_name.el = old_user.name_el
        new_user.first_name.en = old_user.name_en
        new_user.first_name.save()
        new_user.last_name.el = old_user.surname_el
        new_user.last_name.en = old_user.surname_en
        new_user.last_name.save()
        new_user.father_name.el = old_user.fathername_el
        new_user.father_name.en = old_user.fathername_en
        new_user.father_name.save()
        new_user.id_passport = old_user.person_id_number
        new_user.mobile_phone_number=old_user.mobile
        new_user.home_phone_number=old_user.phone
        new_user.email = old_user.email
        logger.info(
            'updated user %s from user_id %s' %
            (new_user.id, old_user.user_id))

    except ApellaUser.DoesNotExist as e:
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

        try:
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
            logger.info(
                'created user %s from user_id %s' %
                (new_user.id, old_user.user_id))
        except IntegrityError as e:
            logger.error(
                'failed to create new user from %s' %  old_user.user_id)
            logger.error(e)
            return

    if password and not new_user.has_usable_password():
        new_user.set_password(password)

    if apella2_shibboleth_id:
        new_user.shibboleth_id = apella2_shibboleth_id
        new_user.shibboleth_migration_key = old_user.migration_key
        new_user.login_method = 'academic'
        new_user.set_unusable_password()

    return new_user


def migrate_user_role(old_user, new_user, login=False):
    role = old_user.role
    if role == 'candidate':
        assistant_professor = \
            OldApellaCandidateAssistantProfessorMigrationData.objects. \
                filter(user_id=old_user.user_id)
        if not assistant_professor:
            migrate_candidate(old_user, new_user)
        else:
            migrate_candidate_to_assistant_professor(old_user, new_user)
        if not login:
            migrate_user_profile_files(old_user, new_user)
            migrate_candidacies(candidate_user=new_user)
    elif role == 'professor':
        migrate_professor(old_user, new_user)
        if not login:
            migrate_user_profile_files(old_user, new_user)
            migrate_candidacies(candidate_user=new_user)
    elif role == 'institutionmanager' and not login:
        institutionmanager = migrate_institutionmanager(old_user, new_user)
        department_ids = Department.objects.filter(
            institution=institutionmanager.institution).values_list(
                'id', flat=True)
        old_positions = OldApellaPositionMigrationData.objects.filter(
            department_id__in=map(str, department_ids))
        for old_position in old_positions:
            migrate_position(old_position, institutionmanager)


STATE_MAPPING = {
    'CANCELLED': 'cancelled',
    'ENTAGMENI': 'posted',
    'ANOIXTI': 'posted',
    'EPILOGI': 'electing',
    'STELEXOMENI': 'successful'
}

@transaction.atomic
def migrate_position(old_position, author):
    subject_area = get_obj(old_position.subject_area_code, SubjectArea)
    old_code = str(subject_area.id) + '.' + old_position.subject_code
    try:
        subject = Subject.objects.get(old_code=old_code)
    except Subject.DoesNotExist:
        logger.error(
            "subject %s does not exist; "
            "position %s failed to migrate" %
            (old_code, old_position.position_serial))
        return

    department = get_obj(old_position.department_id, Department)
    if not author:
        author = InstitutionManager.objects.get(
            institution=department.institution,
            user__role='institutionmanager')

    fek_posted_at = datetime.strptime(
        old_position.gazette_publication_date, '%Y-%m-%d')
    fek_posted_at = at_day_start(fek_posted_at, otz)
    starts_at = datetime.strptime(
        old_position.opening_date, '%Y-%m-%d')
    starts_at = at_day_start(starts_at, otz)
    ends_at = datetime.strptime(
        old_position.closing_date, '%Y-%m-%d')
    ends_at = at_day_end(ends_at, otz)

    position_dep_number = department.dep_number if department.dep_number \
        else 0

    state = 'posted'
    if old_position.state in STATE_MAPPING:
        state = STATE_MAPPING.get(old_position.state)

    try:
        new_position = Position.objects.get(
            old_code=old_position.position_serial)
        new_position.title = old_position.title
        new_position.description = old_position.description
        new_position.subject = subject
        new_position.subject_area = subject_area
        new_position.author = author
        new_position.discipline = old_position.subject_id
        new_position.department = department
        new_position.department_dep_number = position_dep_number
        new_position.fek = old_position.gazette_publication_url
        new_position.fek_posted_at = fek_posted_at
        new_position.state = state
        new_position.starts_at = starts_at
        new_position.ends_at = ends_at
        new_position.save()

    except Position.DoesNotExist:
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
                department_dep_number=position_dep_number,
                fek=old_position.gazette_publication_url,
                fek_posted_at=fek_posted_at,
                state=state,
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
        except MultipleObjectsReturned:
            logger.error(
                'MultipleObjectsReturned: cannot migrate candidacy %s: position %s' %
                (old_candidacy.candidacy_serial,
                    old_candidacy.position_serial))
            continue

        migrate_candidacy(old_candidacy, new_candidate, new_position)


@transaction.atomic
def migrate_candidacy_files(new_candidacy):
    old_candidacy_files = OldApellaCandidacyFileMigrationData. \
        objects.filter(candidacy_serial=str(new_candidacy.old_candidacy_id))

    remove_attr_files(new_candidacy)
    for old_file in old_candidacy_files:
        migrate_file(
            old_file, new_candidacy.candidate, 'candidacy', new_candidacy.id)


@transaction.atomic
def migrate_candidacy(old_candidacy, new_candidate, new_position):

    state = 'cancelled' if old_candidacy.withdrawn_at else 'posted'
    if old_candidacy.withdrawn_at:
        withdrawn_at = datetime.strptime(
            old_candidacy.withdrawn_at, '%Y-%m-%d')
        withdrawn_at = at_day_start(withdrawn_at, otz)
    else:
        withdrawn_at = datetime.utcnow()

    candidacies = Candidacy.objects.filter(
        old_candidacy_id=int(old_candidacy.candidacy_serial))
    if candidacies:
        candidacy = candidacies.order_by('id').annotate(Min('id'))[0]
        candidacy.state = state
        candidacy.updated_at = withdrawn_at
        candidacy.others_can_view = bool(
            re.match('t', old_candidacy.open_to_other_candidates, re.I))
        candidacy.submitted_at = old_candidacy.submitted_at
        candidacy.save()
    else:
        candidacy = Candidacy.objects.create(
            candidate=new_candidate,
            position=new_position,
            state=state,
            others_can_view=bool(
                re.match('t', old_candidacy.open_to_other_candidates, re.I)),
            old_candidacy_id=int(old_candidacy.candidacy_serial),
            submitted_at=old_candidacy.submitted_at,
            updated_at=withdrawn_at)

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


def migrate_candidate_to_assistant_professor(old_user, new_user):
    ap = OldApellaCandidateAssistantProfessorMigrationData.objects.get(
        user_id=old_user.user_id)
    institution = get_obj(ap.institution, Institution)
    department = get_obj(ap.department, Department)
    old_user.professor_institution_id = institution.id
    old_user.professor_department_id = department.id
    old_user.professor_rank = 'Assistant Professor'
    old_user.professor_appointment_gazette_url = ap.fek
    old_user.professor_subject_from_appointment = ap.discipline_from_fek
    new_user.role = 'professor'
    new_user.save()
    professor = migrate_professor(old_user, new_user)
    logger.info(
        'created assistant professor %s' % professor.id)
    return professor

def migrate_user_interests():
    old_subs_user_ids = \
        OldApellaAreaSubscriptions.objects.values_list(
            'user_id', flat=True).distinct()

    for old_user_id in old_subs_user_ids:
        try:
            new_user = ApellaUser.objects.get(old_user_id=old_user_id)
        except ApellaUser.DoesNotExist:
            logger.info('could not find ApellaUser with old user id %r' %
                old_user_id)
            continue
        try:
            new_ui = UserInterest.objects.get(user=new_user)
        except UserInterest.DoesNotExist:
            new_ui = UserInterest.objects.create(user=new_user)

        user_subs = OldApellaAreaSubscriptions.objects.filter(
            user_id=old_user_id)
        departments_added = False
        for user_sub in user_subs:
            if user_sub.subject_id and user_sub.area_id:
                subject_area = get_obj(
                    user_sub.area_id, SubjectArea)
                old_code = \
                    str(subject_area.id) + '.' + user_sub.subject_id
                try:
                    subject = Subject.objects.get(old_code=old_code)
                except Subject.DoesNotExist:
                    logger.error(
                        "subject %s does not exist", old_code)
                    continue
                new_ui.subject.add(subject)
            if user_sub.departments_id and not departments_added:
                departments_added = True
                dep_ids = user_sub.departments_id[1:-1]
                dep_ids = [int(x) for x in dep_ids.split(',')]
                for dep_id in dep_ids:
                    department = get_obj(dep_id, Department)
                    new_ui.department.add(department)
            new_ui.save()
