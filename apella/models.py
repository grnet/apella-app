import os
from datetime import timedelta

from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, \
    UserManager
from django.conf import settings
from django.core import validators
from django.core.files.storage import FileSystemStorage

from apella.validators import validate_dates_interval
from apella import common
from apella.helpers import assistant_can_edit, professor_participates,\
    position_is_latest


class MultiLangFields(models.Model):
    el = models.CharField(max_length=500, blank=True, null=True)
    en = models.CharField(max_length=500, blank=True, null=True)


class RegistrationToken(models.Model):
    token = models.CharField(max_length=255, unique=True, blank=True)
    identifier = models.CharField(max_length=255, blank=True)
    data = models.TextField(blank=True)
    remote_data = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


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
    activated_at = models.DateTimeField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(null=True, default=None)

    date_joined = models.DateTimeField(default=timezone.now)
    id_passport = models.CharField(max_length=20, blank=True)
    mobile_phone_number = models.CharField(max_length=30, blank=True)
    home_phone_number = models.CharField(max_length=30, blank=True)
    role = models.CharField(
        choices=common.USER_ROLES, max_length=20, default='candidate')
    login_method = models.CharField(max_length=20, default='password',
                                    blank=False)

    objects = UserManager()

    can_set_academic = models.BooleanField(default=False)
    can_upgrade_role = models.BooleanField(default=False)

    shibboleth_enabled_at = models.DateTimeField(null=True, default=None)
    shibboleth_id = models.CharField(
        max_length=255, unique=True, null=True, default=None)
    shibboleth_registration_key = models.CharField(
        max_length=255, null=True, default=None)
    shibboleth_migration_key = models.CharField(
        max_length=255, null=True, default=None)
    remote_data = models.TextField(blank=True)
    old_user_id = models.IntegerField(null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    @property
    def apimas_roles(self):
        return [self.role]

    def is_helpdeskadmin(self):
        return self.role == 'helpdeskadmin'

    def is_helpdeskuser(self):
        return self.role == 'helpdeskuser'

    def is_helpdesk(self):
        return self.is_helpdeskadmin() or self.is_helpdeskuser()

    def is_institutionmanager(self):
        return self.role == 'institutionmanager'

    def is_assistant(self):
        return self.role == 'assistant'

    def is_manager(self):
        return self.is_institutionmanager() or self.is_assistant()

    def is_professor(self):
        return self.role == 'professor'

    def is_academic_professor(self):
        return self.is_professor() and not self.professor.is_foreign

    def is_foreign_professor(self):
        return self.is_professor() and self.professor.is_foreign

    def is_candidate(self):
        return self.role == 'candidate'

    def check_resource_state_owned(self, row, request, view):
        return request.user.id == self.id

    def check_resource_state_is_candidate(self, row, request, view):
        return request.user.is_manager() and \
            (self.is_candidate() or self.is_professor())

    def check_resource_state_is_cocandidate(self, row, request, view):
        if not self.is_professor() and not self.is_candidate():
            return False
        user = request.user
        candidacy_set = user.candidacy_set.filter(
            state='posted')
        if not candidacy_set:
            return False

        position_ids = candidacy_set.values_list(
            'position', flat=True)
        user_candidacy_set = self.candidacy_set.filter(
            state='posted')
        return user_candidacy_set.filter(position__in=position_ids)


def generate_filename(self, filename):
    url = "%s/%s/%d/%s/%s" % (
            self.owner.username,
            self.source,
            self.source_id,
            self.file_kind,
            filename)
    return url


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class ApellaFile(models.Model):
    owner = models.ForeignKey(ApellaUser)
    source = models.CharField(choices=common.FILE_SOURCE, max_length=30)
    source_id = models.IntegerField()
    file_kind = models.CharField(choices=common.FILE_KINDS, max_length=40)
    file_path = models.FileField(
        upload_to=generate_filename,
        storage=OverwriteStorage(), max_length=255)
    description = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(ApellaFile, self).save(*args, **kwargs)

    def check_resource_state_owned(self, row, request, view):
        return request.user == self.owner

    def check_resource_state_others_can_view(self, row, request, view):
        user = request.user
        if not self.is_candidacy_file:
            return False
        user_candidacies_positions_ids = user.candidacy_set.filter(
            state='posted').values_list('position', flat=True)

        if self.apella_candidacy_cv_files.filter(
                others_can_view=True).exists():
            return self.apella_candidacy_cv_files.filter(
                others_can_view=True,
                position__in=user_candidacies_positions_ids).exists()
        if self.apella_candidacy_diploma_files.filter(
                others_can_view=True).exists():
            return self.apella_candidacy_diploma_files.filter(
                others_can_view=True,
                position__in=user_candidacies_positions_ids).exists()
        if self.apella_candidacy_publication_files.filter(
                others_can_view=True).exists():
            return self.apella_candidacy_publication_files.filter(
                others_can_view=True,
                position__in=user_candidacies_positions_ids).exists()
        return False

    def check_resource_state_owned_by_manager(self, row, request, view):
        user = request.user
        if user == self.owner:
            return True
        if self.owner.is_assistant() and user.is_manager():
            return True
        if user.is_manager() and self.is_candidacy_file:
            user_department_ids = Department.objects.filter(
                institution=user.institutionmanager.institution). \
                    values_list('id', flat=True)
            if self.apella_candidacy_cv_files.filter(
                    position__department_id__in=user_department_ids,
                    state='posted') or \
                self.apella_candidacy_diploma_files.filter(
                    position__department_id__in=user_department_ids,
                    state='posted') or \
                self.apella_candidacy_publication_files.filter(
                    position__department_id__in=user_department_ids,
                    state='posted'):
                return True
        return False

    def check_resource_state_owned_free(self, row, request, view):
        user = request.user
        is_owner = self.owner == user
        is_verified = True
        if user.is_professor():
            is_verified = user.professor.is_verified or \
                user.professor.verification_pending
        elif user.is_candidate():
            is_verified = user.candidate.is_verified or \
                user.candidate.verification_pending
        elif user.is_manager():
            is_verified = user.institutionmanager.is_verified or \
                user.institutionmanager.verification_pending

        if (hasattr(self, 'id_passport_file') or
                hasattr(self, 'professor_cv_file')) and \
                is_owner and not is_verified:
            return True
        if self.is_profile_file and is_owner:
            return True
        return False

    @property
    def is_candidacy_file(self):
        return self.apella_candidacy_cv_files.exists() or \
            self.apella_candidacy_diploma_files.exists() or \
            self.apella_candidacy_publication_files.exists()

    @property
    def is_profile_file(self):
        return self.apella_candidate_cv_files.exists() or \
            self.apella_candidate_diploma_files.exists() or \
            self.apella_candidate_publication_files.exists() or \
            self.apella_professor_cv_files.exists() or \
            self.apella_professor_diploma_files.exists() or \
            self.apella_professor_publication_files.exists()

    @property
    def filename(self):
        return self.file_path.name.split("/")[-1]


class Institution(models.Model):
    category = models.CharField(
        choices=common.INSTITUTION_CATEGORIES,
        max_length=30, default='Institution')
    organization = models.URLField(blank=True)
    regulatory_framework = models.URLField(blank=True)
    title = models.ForeignKey(MultiLangFields)
    has_shibboleth = models.BooleanField(default=False)
    idp = models.CharField(max_length=255, blank=True)
    schac_home_organization = models.CharField(max_length=255, blank=True)

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

    def check_resource_state_owned_by_assistant(self, row, request, view):
        user = request.user
        return self in user.institutionmanager.departments.all() and \
            user.institutionmanager.can_create_positions


class SubjectArea(models.Model):
    title = models.ForeignKey(MultiLangFields)


class Subject(models.Model):
    area = models.ForeignKey(SubjectArea)
    title = models.ForeignKey(MultiLangFields)


class UserProfile(models.Model):
    user = models.OneToOneField(ApellaUser)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    verification_pending = models.BooleanField(default=False)
    verification_request = models.DateTimeField(null=True, blank=True)
    is_rejected = models.BooleanField(default=False)
    rejected_reason = models.TextField(null=True, blank=True)
    changes_request = models.DateTimeField(null=True, blank=True)

    @property
    def email(self):
        return self.user.email

    class Meta:
        abstract = True


class CandidateProfile(models.Model):
    cv = models.ForeignKey(
        ApellaFile, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_cv_files')
    diplomas = models.ManyToManyField(
        ApellaFile, blank=True,
        related_name='%(app_label)s_%(class)s_diploma_files')
    publications = models.ManyToManyField(
        ApellaFile, blank=True,
        related_name='%(app_label)s_%(class)s_publication_files')

    class Meta:
        abstract = True


class Professor(UserProfile, CandidateProfile):
    institution = models.ForeignKey(
        Institution, on_delete=models.PROTECT, blank=True, null=True)
    institution_freetext = models.CharField(max_length=255, blank=True)
    department = models.ForeignKey(Department, blank=True, null=True)
    rank = models.CharField(
        choices=common.RANKS, max_length=30, blank=True)
    is_foreign = models.BooleanField(default=False)
    speaks_greek = models.BooleanField(default=True)
    cv_url = models.URLField(blank=True)
    cv_professor = models.ForeignKey(
        ApellaFile, blank=True, null=True,
        related_name='professor_cv_file', on_delete=models.SET_NULL)
    fek = models.CharField(max_length=255, blank=True, null=True)
    discipline_text = models.CharField(max_length=300, blank=True)
    discipline_in_fek = models.BooleanField(default=True)

    def check_resource_state_owned(self, row, request, view):
        return request.user.id == self.user.id

    @property
    def active_elections(self):
        return self.committee_duty.filter(
            Q(state='posted') | Q(state='electing')).count() + \
            self.electorparticipation_set.filter(
                Q(position__state='posted') |
                Q(position__state='electing')).count()

    def save(self, *args, **kwargs):
        self.user.role = 'professor'
        super(Professor, self).save(*args, **kwargs)


class Candidate(UserProfile, CandidateProfile):

    id_passport_file = models.ForeignKey(
        ApellaFile, blank=True, null=True,
        related_name='id_passport_file', on_delete=models.SET_NULL)

    def check_resource_state_owned(self, row, request, view):
        return request.user.id == self.user.id

    def save(self, *args, **kwargs):
        self.user.role = 'candidate'
        super(Candidate, self).save(*args, **kwargs)


class InstitutionManager(UserProfile):
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    departments = models.ManyToManyField(Department, blank=True)
    authority = models.CharField(
        choices=common.AUTHORITIES, max_length=30,
        blank=True, null=True)
    authority_full_name = models.CharField(
        max_length=255, blank=True, null=True)
    manager_role = models.CharField(
        choices=common.MANAGER_ROLES, max_length=20,
        default="institutionmanager")
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
    can_create_registries = models.BooleanField(default=False)
    can_create_positions = models.BooleanField(default=False)
    is_secretary = models.BooleanField(default=False)

    def check_resource_state_owned(self, row, request, view):
        return InstitutionManager.objects.filter(
            user_id=request.user.id,
            institution_id=self.institution.id,
            manager_role='institutionmanager').exists()

    def check_resource_state_owned_by_assistant(
            self, row, request, view):
        return self.user.id == request.user.id

    def save(self, *args, **kwargs):
        self.user.role = self.manager_role
        super(InstitutionManager, self).save(*args, **kwargs)


class ProfessorRank(models.Model):
    rank = models.ForeignKey(MultiLangFields)


class Position(models.Model):
    code = models.CharField(max_length=255)
    old_code = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    discipline = models.TextField()
    ranks = models.ManyToManyField(ProfessorRank, blank=True)
    author = models.ForeignKey(
            InstitutionManager, related_name='authored_positions',
            blank=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    subject_area = models.ForeignKey(SubjectArea, on_delete=models.PROTECT)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    fek = models.URLField()
    fek_posted_at = models.DateTimeField()

    electors = models.ManyToManyField(
            Professor, blank=True, through='ElectorParticipation')
    committee = models.ManyToManyField(
            Professor, blank=True, related_name='committee_duty')
    elected = models.ForeignKey(
            ApellaUser, blank=True, null=True,
            related_name='elected_positions')
    second_best = models.ForeignKey(
            ApellaUser, blank=True, null=True,
            related_name='second_best_positions')

    state = models.CharField(
        choices=common.POSITION_STATES, max_length=30, default='posted')
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    department_dep_number = models.IntegerField()
    electors_meeting_to_set_committee_date = models.DateField(
        blank=True, null=True)
    electors_meeting_date = models.DateField(blank=True, null=True)
    electors_set_file = models.ForeignKey(
        ApellaFile, blank=True, null=True,
        related_name='electors_set_files', on_delete=models.SET_NULL)
    committee_set_file = models.ForeignKey(
        ApellaFile, blank=True, null=True,
        related_name='committee_set_files', on_delete=models.SET_NULL)
    committee_proposal = models.ForeignKey(
        ApellaFile, blank=True, null=True,
        related_name='committee_proposal_files', on_delete=models.SET_NULL)
    committee_note = models.ForeignKey(
        ApellaFile, blank=True, null=True,
        related_name='committee_note_files', on_delete=models.SET_NULL)
    electors_meeting_proposal = models.ForeignKey(
        ApellaFile, blank=True, null=True,
        related_name='electors_meeting_proposal_files',
        on_delete=models.SET_NULL)
    nomination_proceedings = models.ForeignKey(
        ApellaFile, blank=True, null=True,
        related_name='nomination_proceedings_files',
        on_delete=models.SET_NULL)
    proceedings_cover_letter = models.ForeignKey(
        ApellaFile, blank=True, null=True,
        related_name='proceedings_cover_letter_files',
        on_delete=models.SET_NULL)
    nomination_act = models.ForeignKey(
        ApellaFile, blank=True, null=True,
        related_name='nomination_act_files', on_delete=models.SET_NULL)
    nomination_act_fek = models.URLField(blank=True)
    revocation_decision = models.ForeignKey(
        ApellaFile, blank=True, null=True,
        related_name='revocation_decision_files', on_delete=models.SET_NULL)
    failed_election_decision = models.ForeignKey(
        ApellaFile, blank=True, null=True,
        related_name='failed_election_decision_files',
        on_delete=models.SET_NULL)
    assistant_files = models.ManyToManyField(
        ApellaFile, blank=True, related_name='position_assistant_files')

    def clean(self, *args, **kwargs):
        validate_dates_interval(
            self.starts_at,
            self.ends_at,
            settings.START_DATE_END_DATE_INTERVAL)
        super(Position, self).clean(*args, **kwargs)

    def check_resource_state_owned(self, row, request, view):
        user = request.user
        if user.id == self.author.user.id:
            return True
        return InstitutionManager.objects.filter(
            user_id=user.id,
            institution_id=self.department.institution.id).exists()

    def check_resource_state_open(self, row, request, view):
        return self.state == 'posted' and self.ends_at > timezone.now()

    def check_resource_state_before_open(self, row, request, view):
        user = request.user
        before_open = self.starts_at > timezone.now()
        if user.is_institutionmanager():
            return before_open
        elif user.is_assistant():
            return before_open and assistant_can_edit(self, user)
        return False

    def check_resource_state_electing(self, row, request, view):
        user = request.user
        is_electing = self.state == 'electing'
        if user.is_institutionmanager():
            return is_electing
        elif user.is_assistant():
            return is_electing and assistant_can_edit(self, user)
        return False

    def check_resource_state_participates(self, row, request, view):
        return professor_participates(request.user, self.id)

    def check_resource_state_is_latest(self, row, request, view):
        return position_is_latest(self)

    def check_resource_state_owned_by_assistant(self, row, request, view):
        return position_is_latest(self) and \
            assistant_can_edit(self, request.user)

    @classmethod
    def check_collection_state_can_create(cls, row, request, view):
        return InstitutionManager.objects.filter(
            user_id=request.user.id,
            manager_role='assistant',
            can_create_positions=True).exists()


class ElectorParticipation(models.Model):
    professor = models.ForeignKey(Professor)
    position = models.ForeignKey(Position)
    is_regular = models.BooleanField(default=True)


class Candidacy(CandidateProfile):
    candidate = models.ForeignKey(ApellaUser)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    state = models.CharField(
        choices=common.CANDIDACY_STATES, max_length=30, default='draft')
    others_can_view = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    code = models.CharField(max_length=255)
    self_evaluation_report = models.ForeignKey(
        ApellaFile, blank=True, null=True,
        related_name='self_evaluation_report', on_delete=models.SET_NULL)
    attachment_files = models.ManyToManyField(
        ApellaFile, blank=True, related_name='attachment_files')
    old_candidacy_id = models.IntegerField(blank=True, null=True)

    def check_resource_state_owned(self, row, request, view):
        return InstitutionManager.objects.filter(
            user_id=request.user.id,
            institution_id=self.position.department.institution.id,
            manager_role='institutionmanager'). \
            exists() or \
            self.candidate.id == request.user.id

    def check_resource_state_owned_by_assistant(self, row, request, view):
        return InstitutionManager.objects.filter(
            user_id=request.user.id,
            manager_role='assistant').exists() and \
            self.position.department in \
            request.user.institutionmanager.departments.all()

    def check_resource_state_others_can_view(self, row, request, view):
        return self.others_can_view

    def check_resource_state_participates(self, row, request, view):
        return professor_participates(request.user, self.position.id)

    def check_resource_state_owned_open(self, row, request, view):
        return self.check_resource_state_owned(row, request, view) \
                and self.position.check_resource_state_open(
                        row, request, view) \
                and self.state == 'posted'

    def before_electors_meeting(self, days):
        position_state = self.position.state
        if position_state == 'posted' or \
                (position_state == 'electing' and not
                    self.position.electors_meeting_date):
            return True
        elif position_state == 'electing' and \
                self.position.electors_meeting_date:
            if self.position.electors_meeting_date - timezone.now() > \
                    timedelta(days=days):
                return True
        return False

    def check_resource_state_five_before_electors_meeting(
            self, row, request, view):
        return self.check_resource_state_owned(row, request, view) and \
            self.before_electors_meeting(5)

    def check_resource_state_one_before_electors_meeting(
            self, row, request, view):
        return self.check_resource_state_owned(row, request, view) and \
            self.before_electors_meeting(1)

    def check_resource_state_after_closed_electors_meeting_open(
            self, row, request, view):
        return self.position.ends_at < timezone.now() and \
            self.before_electors_meeting(0)


class Registry(models.Model):
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    type = models.CharField(
        choices=common.REGISTRY_TYPES, max_length=20, default='internal')
    members = models.ManyToManyField(Professor)
    registry_set_decision_file = models.ForeignKey(
        ApellaFile, blank=True, null=True,
        related_name='registry_set_decision_files', on_delete=models.SET_NULL)

    class Meta:
        # Each department can have only one internal and one external registry
        unique_together = (("department", "type"),)

    def check_resource_state_owned(self, row, request, view):
        return InstitutionManager.objects.filter(
            user_id=request.user.id,
            institution_id=self.department.institution.id).exists()

    def check_resource_state_can_create_owned(self, row, request, view):
        return InstitutionManager.objects.filter(
            user_id=request.user.id,
            institution_id=self.department.institution.id,
            can_create_registries=True).exists()

    @classmethod
    def check_collection_state_can_create(cls, row, request, view):
        return InstitutionManager.objects.filter(
            user_id=request.user.id,
            manager_role='assistant',
            can_create_registries=True).exists()


class UserInterest(models.Model):
    user = models.ForeignKey(ApellaUser)
    area = models.ManyToManyField(SubjectArea, blank=True)
    subject = models.ManyToManyField(Subject, blank=True)
    institution = models.ManyToManyField(Institution, blank=True)
    department = models.ManyToManyField(Department, blank=True)

    def check_resource_state_owned(self, row, request, view):
        return request.user.id == self.user.id


from migration_models import (
    OldApellaUserMigrationData,
    OldApellaFileMigrationData,
    OldApellaPositionMigrationData,
    OldApellaCandidacyFileMigrationData,
    OldApellaCandidacyMigrationData,
    OldApellaInstitutionMigrationData,
    OldApellaCandidateAssistantProfessorMigrationData
)
