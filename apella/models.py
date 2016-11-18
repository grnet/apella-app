from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, \
    UserManager
from django.conf import settings
from django.core import validators

from apella.validators import before_today_validator, after_today_validator,\
    validate_dates_interval, validate_position_dates
from apella import common


class MultiLangFields(models.Model):
    el = models.CharField(max_length=500)
    en = models.CharField(max_length=500)


class ApellaUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=30, unique=True,
        help_text='Required. 30 characters or fewer. Letters, digits and '
                  '@/./+/-/_ only.',
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$',
                                      'Enter a valid username. '
                                      'This value may contain only letters,'
                                      ' numbers '
                                      'and @/./+/-/_ characters.',
                                      'invalid'),
        ],
        error_messages={
            'unique': "A user with that username already exists.",
        }
    )
    first_name = models.ForeignKey(MultiLangFields, related_name='first_name')
    last_name = models.ForeignKey(MultiLangFields, related_name='last_name')
    father_name = models.ForeignKey(
        MultiLangFields, related_name='father_name')
    email = models.EmailField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    id_passport = models.CharField(max_length=20)
    mobile_phone_number = models.CharField(max_length=30)
    home_phone_number = models.CharField(max_length=30)
    role = models.CharField(
        choices=common.USER_ROLES, max_length=20, default='candidate')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Institution(models.Model):
    category = models.CharField(
        choices=common.INSTITUTION_CATEGORIES,
        max_length=30, default='Institution')
    organization = models.URLField(blank=True)
    regulatory_framework = models.URLField(blank=True)
    title = models.ForeignKey(MultiLangFields)

    def check_object_state_owned(self, row, request, view):
        return InstitutionManager.objects.filter(
                user_id=request.user.id,
                institution_id=self.id).exists()


class School(models.Model):
    institution = models.ForeignKey(Institution)
    title = models.ForeignKey(MultiLangFields)


class Department(models.Model):
    school = models.ForeignKey(School, blank=True, null=True)
    institution = models.ForeignKey(Institution)
    title = models.ForeignKey(MultiLangFields)


class SubjectArea(models.Model):
    title = models.ForeignKey(MultiLangFields)


class Subject(models.Model):
    area = models.ForeignKey(SubjectArea)
    title = models.ForeignKey(MultiLangFields)


class ApellaFile(models.Model):
    file_kind = models.CharField(choices=common.FILE_KINDS, max_length=40)
    file_path = models.CharField(max_length=500)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(ApellaFile, self).save(*args, **kwargs)


class Professor(models.Model):
    user = models.OneToOneField(ApellaUser)
    institution = models.ForeignKey(Institution)
    department = models.ForeignKey(Department, blank=True, null=True)
    rank = models.CharField(
        choices=common.RANKS, max_length=30)
    is_foreign = models.BooleanField(default=False)
    speaks_greek = models.BooleanField(default=True)
    cv_url = models.URLField(blank=True)
    fek = models.URLField()
    discipline_text = models.CharField(max_length=300)
    discipline_in_fek = models.BooleanField(default=True)


class Candidate(models.Model):
    user = models.OneToOneField(ApellaUser)


class UserFiles(models.Model):
    apella_file = models.ForeignKey(ApellaFile, related_name='user_files')
    apella_user = models.ForeignKey(ApellaUser, related_name='user_files')
    deleted = models.BooleanField(default=False, db_index=True)


class InstitutionManager(models.Model):
    user = models.OneToOneField(ApellaUser)
    institution = models.ForeignKey(Institution)
    authority = models.CharField(choices=common.AUTHORITIES, max_length=1)
    authority_full_name = models.CharField(max_length=150)
    manager_role = models.CharField(
        choices=common.MANAGER_ROLES, max_length=1)


class Position(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    discipline = models.CharField(max_length=300)
    author = models.ForeignKey(
            InstitutionManager, related_name='authored_positions')
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    subject_area = models.ForeignKey(SubjectArea, on_delete=models.PROTECT)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    fek = models.URLField()
    fek_posted_at = models.DateTimeField(validators=[before_today_validator])

    assistants = models.ManyToManyField(
            InstitutionManager, blank=True, related_name='assistant_duty')
    electors = models.ManyToManyField(
            Professor, blank=True, related_name='elector_duty')
    committee = models.ManyToManyField(
            Professor, blank=True, related_name='committee_duty')
    elected = models.ForeignKey(
            ApellaUser, blank=True, null=True,
            related_name='elected_positions')

    state = models.CharField(
        choices=common.POSITION_STATES, max_length=30, default='posted')
    starts_at = models.DateTimeField(validators=[after_today_validator])
    ends_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def clean(self, *args, **kwargs):
        validate_dates_interval(
            self.starts_at,
            self.ends_at,
            settings.START_DATE_END_DATE_INTERVAL)
        super(Position, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(Position, self).save(*args, **kwargs)

    def check_object_state_owned(self, row, request, view):
        return InstitutionManager.objects.filter(
            user_id=request.user.id,
            institution_id=self.department.institution.id).exists()

    def check_object_state_open(self, row, request, view):
        return self.state == 'posted' and self.starts_at > timezone.now()

    def check_object_state_participates(self, row, request, view):
        try:
            professor = Professor.objects.get(user_id=request.user.id)
        except Professor.DoesNotExist:
            return False
        has_elector_duty = professor.elector_duty.filter(id=self.id)
        if has_elector_duty:
            return True
        has_committee_duty = professor.committee_duty.filter(id=self.id)
        if has_committee_duty:
            return True
        return False


class PositionFiles(models.Model):
    position_file = models.ForeignKey(
        ApellaFile, related_name='position_files')
    position = models.ForeignKey(Position, related_name='position_files')
    deleted = models.BooleanField(default=False, db_index=True)


class Candidacy(models.Model):
    candidate = models.ForeignKey(ApellaUser)
    position = models.ForeignKey(Position)
    state = models.CharField(
        choices=common.CANDIDACY_STATES, max_length=1, default='2')
    others_can_view = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

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
    department = models.ForeignKey(Department)
    type = models.CharField(
        choices=common.REGISTRY_TYPES, max_length=1, default='1')
    members = models.ManyToManyField(Professor)

    class Meta:
        # Each department can have only one internal and one external registry
        unique_together = (("department", "type"),)
