from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, \
    UserManager
from django.conf import settings
from django.core import validators

from apella.validators import before_today_validator, after_today_validator,\
    validate_dates_interval, validate_position_dates
from apella import common


def professor_participates(user_id, position_id):
    try:
        professor = Professor.objects.get(user_id=user_id)
    except Professor.DoesNotExist:
        return False
    has_elector_duty = professor.elector_duty.filter(id=position_id)
    if has_elector_duty:
        return True
    has_committee_duty = \
        professor.committee_duty.filter(id=position_id)
    if has_committee_duty:
        return True
    return False


class MultiLangFields(models.Model):
    el = models.CharField(max_length=500, blank=True, null=True)
    en = models.CharField(max_length=500, blank=True, null=True)


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
        MultiLangFields, related_name='father_name', blank=True, null=True)
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': "A user with that email already exists.",
        }
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    id_passport = models.CharField(max_length=20, blank=True)
    mobile_phone_number = models.CharField(max_length=30, blank=True)
    home_phone_number = models.CharField(max_length=30, blank=True)
    role = models.CharField(
        choices=common.USER_ROLES, max_length=20, default='candidate')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    @property
    def apimas_roles(self):
        return [self.role]


class Institution(models.Model):
    category = models.CharField(
        choices=common.INSTITUTION_CATEGORIES,
        max_length=30, default='Institution')
    organization = models.URLField(blank=True)
    regulatory_framework = models.URLField(blank=True)
    title = models.ForeignKey(MultiLangFields)

    def check_resource_state_owned(self, row, request, view):
        return InstitutionManager.objects.filter(
                user_id=request.user.id,
                institution_id=self.id).exists()


class School(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    title = models.ForeignKey(MultiLangFields)


class Department(models.Model):
    school = models.ForeignKey(School, blank=True, null=True)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    title = models.ForeignKey(MultiLangFields)
    dep_number = models.IntegerField(blank=True, null=True)


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


class UserProfile(models.Model):
    user = models.OneToOneField(ApellaUser)
    is_active = models.BooleanField(default=False)
    activated_at = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    is_rejected = models.BooleanField(default=False)
    rejected_reason = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


class Professor(UserProfile):
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, blank=True, null=True)
    rank = models.CharField(
        choices=common.RANKS, max_length=30)
    is_foreign = models.BooleanField(default=False)
    speaks_greek = models.BooleanField(default=True)
    cv_url = models.URLField(blank=True)
    fek = models.URLField()
    discipline_text = models.CharField(max_length=300)
    discipline_in_fek = models.BooleanField(default=True)


class Candidate(UserProfile):
    pass


class UserFiles(models.Model):
    apella_file = models.ForeignKey(ApellaFile, related_name='user_files')
    apella_user = models.ForeignKey(ApellaUser, related_name='user_files')
    deleted = models.BooleanField(default=False, db_index=True)


class InstitutionManager(UserProfile):
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    authority = models.CharField(choices=common.AUTHORITIES, max_length=1)
    authority_full_name = models.CharField(max_length=150)
    manager_role = models.CharField(
        choices=common.MANAGER_ROLES, max_length=20)
    sub_first_name = models.ForeignKey(
        MultiLangFields, related_name='sub_first_name',
        blank=True, null=True)
    sub_last_name = models.ForeignKey(
        MultiLangFields, related_name='sub_last_name',
        blank=True, null=True)
    sub_father_name = models.ForeignKey(
        MultiLangFields, related_name='sub_father_name',
        blank=True, null=True)
    sub_email = models.EmailField(blank=True, null=True)
    sub_mobile_phone_number = models.CharField(
        max_length=30, blank=True, null=True)
    sub_home_phone_number = models.CharField(
        max_length=30, blank=True, null=True)

    def check_resource_state_owned(self, row, request, view):
        return InstitutionManager.objects.filter(
            user_id=request.user.id,
            institution_id=self.institution.id,
            manager_role='manager').exists()


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
    department_dep_number = models.IntegerField()

    def clean(self, *args, **kwargs):
        validate_dates_interval(
            self.starts_at,
            self.ends_at,
            settings.START_DATE_END_DATE_INTERVAL)
        super(Position, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(Position, self).save(*args, **kwargs)

    def check_resource_state_owned(self, row, request, view):
        return InstitutionManager.objects.filter(
            user_id=request.user.id,
            institution_id=self.department.institution.id).exists()

    def check_resource_state_open(self, row, request, view):
        return self.state == 'posted' and self.ends_at > timezone.now()

    def check_resource_state_before_open(self, row, request, view):
        return self.starts_at > timezone.now()

    def check_resource_state_closed(self, row, request, view):
        return self.starts_at < timezone.now()

    def check_resource_state_electing(self, row, request, view):
        return self.state == 'posted' and self.starts_at < timezone.now()

    def check_resource_state_participates(self, row, request, view):
        return professor_participates(request.user.id, self.id)


class PositionFiles(models.Model):
    position_file = models.ForeignKey(
        ApellaFile, related_name='position_files')
    position = models.ForeignKey(Position, related_name='position_files')
    deleted = models.BooleanField(default=False, db_index=True)


class Candidacy(models.Model):
    candidate = models.ForeignKey(ApellaUser)
    position = models.ForeignKey(Position)
    state = models.CharField(
        choices=common.CANDIDACY_STATES, max_length=30, default='posted')
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

    def check_resource_state_owned(self, row, request, view):
        return InstitutionManager.objects.filter(
                user_id=request.user.id,
                institution_id=self.position.department.institution.id). \
                exists() or \
                self.candidate.id == request.user.id

    def check_resource_state_others_can_view(self, row, request, view):
        return self.others_can_view

    def check_resource_state_participates(self, row, request, view):
        return professor_participates(request.user.id, self.position.id)

    def check_resource_state_owned_open(self, row, request, view):
        return self.check_resource_state_owned(row, request, view) \
                and self.position.check_resource_state_open(
                        row, request, view) \
                and self.state == 'cancelled'


class CandidacyFiles(object):
    candidacy_file = models.ForeignKey(
        ApellaFile, related_name='candidacy_files')
    candidacy = models.ForeignKey(Candidacy, related_name='candidacy_files')
    deleted = models.BooleanField(default=False, db_index=True)


class Registry(models.Model):
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    type = models.CharField(
        choices=common.REGISTRY_TYPES, max_length=1, default='1')
    members = models.ManyToManyField(Professor)

    class Meta:
        # Each department can have only one internal and one external registry
        unique_together = (("department", "type"),)

    def check_resource_state_owned(self, row, request, view):
        return InstitutionManager.objects.filter(
            user_id=request.user.id,
            institution_id=self.department.institution.id).exists()


class UserInterest(models.Model):
    user = models.ForeignKey(ApellaUser)
    area = models.ManyToManyField(SubjectArea, blank=True)
    subject = models.ManyToManyField(Subject, blank=True)
    institution = models.ManyToManyField(Institution, blank=True)
    department = models.ManyToManyField(Department, blank=True)
