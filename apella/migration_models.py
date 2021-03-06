import hashlib
import base64

from django.db import models


class OldApellaUserMigrationData(models.Model):
    migration_key = models.TextField(null=True, default=None)
    user_id = models.TextField()
    username = models.TextField()
    permanent_auth_token = models.TextField(null=True)
    passwd = models.TextField()
    passwd_salt = models.TextField()
    shibboleth_id = models.TextField()
    role = models.TextField()
    name_el = models.TextField()
    surname_el = models.TextField()
    fathername_el = models.TextField()
    name_en = models.TextField()
    surname_en = models.TextField()
    fathername_en = models.TextField()
    email = models.TextField()
    mobile = models.TextField()
    phone = models.TextField()
    person_id_number = models.TextField()
    is_foreign = models.TextField()
    speaks_greek = models.TextField()
    professor_subject_id = models.TextField()
    professor_rank = models.TextField()
    professor_institution_id = models.TextField()
    professor_institution_freetext = models.TextField()
    professor_department_id = models.TextField()
    professor_appointment_gazette_url = models.TextField()
    professor_subject_from_appointment = models.TextField()
    professor_subject_optional_freetext = models.TextField()
    professor_institution_cv_url = models.TextField()
    manager_institution_id = models.TextField()
    manager_appointer_authority = models.TextField()
    manager_appointer_fullname = models.TextField()
    manager_deputy_name_el = models.TextField()
    manager_deputy_surname_el = models.TextField()
    manager_deputy_fathername_el = models.TextField()
    manager_deputy_name_en = models.TextField()
    manager_deputy_surname_en = models.TextField()
    manager_deputy_fathername_en = models.TextField()
    manager_deputy_mobile = models.TextField()
    manager_deputy_phone = models.TextField()
    manager_deputy_email = models.TextField()
    role_status = models.TextField(default='UNAPPROVED')
    migrated_at = models.DateTimeField(null=True, blank=True)

    @staticmethod
    def encode_password(password, salt):
        if not isinstance(password, str):
            password = password.encode('iso-8859-1')

        if not isinstance(salt, str):
            salt = salt.encode('iso-8859-1')

        hasher = hashlib.sha1(password + salt)
        return hasher.digest()

    def check_password(self, password):
        if password == self.permanent_auth_token:
            return

        salt = self.passwd_salt
        encoded = self.encode_password(password, salt)
        encoded = base64.encodestring(encoded).strip()
        if encoded != self.passwd:
            m = "Wrong password for user {0!r}".format(self.username)
            raise ValueError(m)

    @classmethod
    def get_users_by_token(cls, permanent_auth_token):
        users = cls.objects.filter(permanent_auth_token=permanent_auth_token)
        return users


class OldApellaFileMigrationData(models.Model):
    user_id = models.TextField(db_index=True)
    header_id = models.TextField()
    file_type = models.TextField()
    file_path = models.TextField()
    file_description = models.TextField()
    original_name = models.TextField()
    updated_at = models.DateTimeField(null=True)


class OldApellaPositionMigrationData(models.Model):
    position_serial = models.TextField(primary_key=True)
    description = models.TextField()
    title = models.TextField()
    subject_id = models.TextField()
    department_id = models.TextField()
    manager_id = models.TextField()
    subject_area_code = models.TextField()
    subject_code = models.TextField()
    gazette_publication_url = models.TextField()
    gazette_publication_date = models.TextField()
    state = models.TextField()
    opening_date = models.TextField()
    closing_date = models.TextField()


class OldApellaCandidacyFileMigrationData(models.Model):
    candidacy_serial = models.TextField(db_index=True)
    position_serial = models.TextField()
    candidate_user_id = models.TextField()
    file_id = models.TextField()
    file_type = models.TextField()
    file_path = models.TextField()
    file_description = models.TextField()
    original_name = models.TextField()
    updated_at = models.DateTimeField(null=True)


class OldApellaCandidacyMigrationData(models.Model):
    candidacy_serial = models.TextField()
    position_serial = models.TextField(db_index=True)
    candidate_user_id = models.TextField(db_index=True)
    open_to_other_candidates = models.TextField()
    submitted_at = models.DateTimeField(null=True)
    withdrawn_at = models.TextField(null=True)


class OldApellaInstitutionMigrationData(models.Model):
    institution_id = models.TextField()
    institution_bylaw_url = models.TextField()
    institution_organization_url = models.TextField()


class OldApellaCandidateAssistantProfessorMigrationData(models.Model):
    user_id = models.TextField()
    surname_el = models.TextField()
    name_el = models.TextField()
    fathername_el = models.TextField()
    email = models.TextField()
    institution = models.TextField()
    department = models.TextField()
    fek = models.TextField()
    discipline_from_fek = models.TextField()


class OldApellaAreaSubscriptions(models.Model):
    user_id = models.TextField()
    version = models.TextField()
    sector_id = models.TextField()
    area_id = models.TextField()
    subject_id = models.TextField()
    area_name = models.TextField()
    subject_name = models.TextField()
    locale = models.TextField()
    departments_id = models.TextField(null=True)
