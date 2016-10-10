from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from apella.validators import before_today_validator, after_today_validator,\
    validate_dates_interval, validate_position_dates
from apella import common


class ApellaUserFields(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=300)
    father_name = models.CharField(max_length=200)

    class Meta:
        abstract = True


class ApellaUserEl(ApellaUserFields):
    pass


class ApellaUserEn(ApellaUserFields):
    pass


class ApellaUser(AbstractUser):

    """
    Model for users of `Apella`.

    It actually inherits from `AbstractUser` class of
    `django.contib.auth.models` which define common fields such as first name,
    last name, email, etc
    """
    role = models.CharField(
        choices=common.USER_ROLES, max_length=1, default='2')
    el = models.ForeignKey(ApellaUserEl, blank=True)
    en = models.ForeignKey(ApellaUserEn, blank=True)
    id_passport = models.CharField(max_length=20, blank=False, null=False)
    mobile_phone_number = models.CharField(max_length=30)
    home_phone_number = models.CharField(max_length=30)


class InstitutionFields(models.Model):
    title = models.CharField(max_length=150, blank=True)

    class Meta:
        abstract = True


class InstitutionEl(InstitutionFields):
    pass


class InstitutionEn(InstitutionFields):
    pass


class Institution(models.Model):
    category = models.CharField(
        choices=common.INSTITUTION_CATEGORIES, blank=False, null=False,
        max_length=15, default='1')
    organization = models.URLField(blank=True)
    regulatory_framework = models.URLField(blank=True)
    el = models.ForeignKey(InstitutionEl, blank=True, null=True)
    en = models.ForeignKey(InstitutionEn, blank=True, null=True)


class SchoolFields(models.Model):
    title = models.CharField(max_length=150, blank=False)

    class Meta:
        abstract = True


class SchoolEl(SchoolFields):
    pass


class SchoolEn(SchoolFields):
    pass


class School(models.Model):
    institution = models.ForeignKey(Institution, blank=False, null=False)
    el = models.ForeignKey(SchoolEl, blank=True, null=True)
    en = models.ForeignKey(SchoolEn, blank=True, null=True)


class DepartmentFields(models.Model):
    title = models.CharField(max_length=150, blank=False)

    class Meta:
        abstract = True


class DepartmentEl(DepartmentFields):
    pass


class DepartmentEn(DepartmentFields):
    pass


class Department(models.Model):
    school = models.ForeignKey(School, blank=True, null=True)
    institution = models.ForeignKey(Institution, blank=False, null=False)
    el = models.ForeignKey(DepartmentEl, blank=True, null=True)
    en = models.ForeignKey(DepartmentEn, blank=True, null=True)


class SubjectAreaFields(models.Model):
    title = models.CharField(max_length=200, blank=True)

    class Meta:
        abstract = True


class SubjectAreaEl(SubjectAreaFields):
    pass


class SubjectAreaEn(SubjectAreaFields):
    pass


class SubjectArea(models.Model):
    el = models.ForeignKey(SubjectAreaEl, blank=True, null=True)
    en = models.ForeignKey(SubjectAreaEn, blank=True, null=True)


class SubjectFields(models.Model):
    title = models.CharField(max_length=200, blank=True)

    class Meta:
        abstract = True


class SubjectEl(SubjectFields):
    pass


class SubjectEn(SubjectFields):
    pass


class Subject(models.Model):
    area = models.ForeignKey(SubjectArea, blank=False, null=False)
    el = models.ForeignKey(SubjectEl, blank=True, null=True)
    en = models.ForeignKey(SubjectEn, blank=True, null=True)


class ApellaFile(models.Model):
    file_kind = models.CharField(choices=common.FILE_KINDS, max_length=1)
    file_path = models.CharField(max_length=500)
    updated_at = models.DateTimeField(blank=False, default=timezone.now)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(ApellaFile, self).save(*args, **kwargs)


class Professor(models.Model):
    user = models.ForeignKey(ApellaUser, blank=False, null=False)
    institution = models.ForeignKey(Institution, blank=False, null=False)
    department = models.ForeignKey(Department, blank=True, null=True)
    rank = models.CharField(
        choices=common.RANKS, blank=False, null=False, max_length=30)
    is_foreign = models.BooleanField(default=False)
    speaks_greek = models.BooleanField(default=True)
    cv_url = models.URLField(blank=True)
    fek = models.URLField(blank=False)
    discipline_text = models.CharField(max_length=300)
    discipline_in_fek = models.BooleanField(default=True)


class Candidate(models.Model):
    user = models.ForeignKey(ApellaUser, blank=False, null=False)


class UserFiles(models.Model):
    apella_file = models.ForeignKey(ApellaFile, related_name='user_files')
    apella_user = models.ForeignKey(ApellaUser, related_name='user_files')
    deleted = models.BooleanField(default=False, db_index=True)


class InstitutionManager(models.Model):
    user = models.ForeignKey(ApellaUser, blank=False, null=False)
    institution = models.ForeignKey(Institution, blank=False, null=False)
    authority = models.CharField(choices=common.AUTHORITIES, max_length=1)
    authority_full_name = models.CharField(max_length=150)
    manager_role = models.CharField(
        choices=common.MANAGER_ROLES, blank=False, max_length=1)


class Position(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=300, blank=False, null=False)
    discipline = models.CharField(max_length=300, blank=False, null=False)
    author = models.ForeignKey(
            InstitutionManager, blank=False, related_name='authored_positions')
    department = models.ForeignKey(Department, blank=False, null=False)
    subject_area = models.ForeignKey(SubjectArea, blank=False, null=False)
    subject = models.ForeignKey(Subject, blank=False, null=False)
    fek = models.URLField(blank=False, null=False)
    fek_posted_at = models.DateTimeField(
        blank=False, null=False, validators=[before_today_validator])

    assistants = models.ManyToManyField(
            InstitutionManager, blank=True, related_name='assistant_duty')
    electors = models.ManyToManyField(
            ApellaUser, blank=True, related_name='elector_duty')
    committee = models.ManyToManyField(
            ApellaUser, blank=True, related_name='committee_duty')
    elected = models.ForeignKey(
            ApellaUser, blank=True, null=True,
            related_name='elected_positions')

    state = models.CharField(
        choices=common.POSITION_STATES, max_length=1, default='2')
    starts_at = models.DateTimeField(
        blank=False, null=False, validators=[after_today_validator])
    ends_at = models.DateTimeField(blank=False, null=False)
    created_at = models.DateTimeField(blank=False, default=timezone.now)
    updated_at = models.DateTimeField(blank=False, default=timezone.now)

    def clean(self, *args, **kwargs):
        validate_dates_interval(
            self.starts_at,
            self.ends_at,
            settings.START_DATE_END_DATE_INTERVAL)
        super(Position, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(Position, self).save(*args, **kwargs)


class PositionFiles(models.Model):
    position_file = models.ForeignKey(
        ApellaFile, related_name='position_files')
    position = models.ForeignKey(Position, related_name='position_files')
    deleted = models.BooleanField(default=False, db_index=True)


class Candidacy(models.Model):
    candidate = models.ForeignKey(ApellaUser, blank=False)
    position = models.ForeignKey(Position, blank=False)
    state = models.CharField(
        choices=common.CANDIDACY_STATES, max_length=1, default='2')
    others_can_view = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(blank=False, default=timezone.now)
    updated_at = models.DateTimeField(blank=False, default=timezone.now)

    def clean(self, *args, **kwargs):
        validate_position_dates(
            self.position.starts_at,
            self.position.ends_at)
        super(Candidacy, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(Candidacy, self).save(*args, **kwargs)


class CandidacyFiles(object):
    candidacy_file = models.ForeignKey(
        ApellaFile, related_name='candidacy_files')
    candidacy = models.ForeignKey(Candidacy, related_name='candidacy_files')
    deleted = models.BooleanField(default=False, db_index=True)


class Registry(models.Model):
    department = models.ForeignKey(Department, blank=False)
    type = models.CharField(
        choices=common.REGISTRY_TYPES, max_length=1, default='1')
    members = models.ManyToManyField(Professor, blank=False, null=False)

    class Meta:
        # Each department can have only one internal and one external registry
        unique_together = (("department", "type"),)
