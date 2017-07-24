import logging
import os
from datetime import timedelta, datetime
from itertools import chain

from django.db import models
from django.db.models import Q, Max, Min
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, \
    UserManager
from django.conf import settings
from django.core import validators
from django.core.files.storage import FileSystemStorage

from apella.validators import validate_dates_interval
from apella import common
from apella.helpers import assistant_can_edit, professor_participates,\
    position_is_latest
from apella.util import safe_path_join

logger = logging.getLogger(__name__)

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
        max_length=255, unique=True,
        help_text='Required. 255 characters or fewer. Letters, digits and '
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

    date_joined = models.DateTimeField(default=datetime.utcnow)
    id_passport = models.CharField(max_length=255, blank=True)
    mobile_phone_number = models.CharField(max_length=255, blank=True)
    home_phone_number = models.CharField(max_length=255, blank=True)
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
    shibboleth_idp = models.CharField(max_length=255, blank=True)
    shibboleth_schac_home_organization = models.CharField(
        max_length=255, blank=True)
    shibboleth_registration_key = models.CharField(
        max_length=255, null=True, default=None)
    shibboleth_migration_key = models.CharField(
        max_length=255, null=True, default=None)
    remote_data = models.TextField(blank=True)
    old_user_id = models.IntegerField(null=True, blank=True)

    has_accepted_terms = models.BooleanField(default=False)
    accepted_terms_at = models.DateTimeField(null=True, blank=True)

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

    def is_ministry(self):
        return self.role == 'ministry'

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
        position_ids = user.candidacy_set.values_list(
            'position', flat=True)
        user_candidacy_set = self.candidacy_set.all()
        return user_candidacy_set.filter(
            position__in=position_ids).exists()

    def check_resource_state_is_dep_candidate(self, row, request, view):
        if not request.user.is_professor():
            return False
        departments = self.candidacy_set.values_list(
            'position__department', flat=True)
        if getattr(request.user.professor, 'department') and \
                request.user.professor.department.id in departments:
            return True
        positions = self.candidacy_set.values_list(
            'position_id', flat=True)
        prof_positions_elector = \
            request.user.professor.electorparticipation_set. \
            values_list('position_id', flat=True)
        prof_positions_committee = \
            request.user.professor.committee_duty. \
            values_list('id', flat=True)
        for pid in positions:
            if pid in prof_positions_committee or \
                    pid in prof_positions_elector:
                return True
        return False


def generate_filename(apellafile, filename):
    ext = os.path.splitext(filename)[1]
    if len(ext) >= 9:
        ext = ''

    path = "%s/%s-%s%s" % (
            apellafile.owner.username,
            apellafile.file_kind,
            apellafile.id,
            ext)
    return path


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name):
        if self.exists(name):
            os.remove(safe_path_join(settings.MEDIA_ROOT, name))
        return name


class ApellaFile(models.Model):
    id = models.BigIntegerField(primary_key=True)
    owner = models.ForeignKey(ApellaUser)
    source = models.CharField(choices=common.FILE_SOURCE, max_length=30)
    source_id = models.IntegerField()
    file_kind = models.CharField(choices=common.FILE_KINDS, max_length=40)
    file_content = models.FileField(
        upload_to=generate_filename, max_length=1024)
    description = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.utcnow)
    file_name = models.CharField(max_length=1024)
    old_file_path = models.CharField(max_length=1024, null=True)

    def save(self, *args, **kwargs):
        super(ApellaFile, self).save(*args, **kwargs)

    def check_resource_state_owned(self, row, request, view):
        return request.user == self.owner

    def check_resource_state_is_candidate(self, row, request, view):
        user = request.user
        if not user.is_candidate():
            return False
        if self.source == 'position':
            candidacies = user.candidacy_set. \
                filter(state='posted'). \
                values_list('position_id', flat=True)
            if self.source_id in candidacies:
                return True
        return False

    def check_resource_state_participates(self, row, request, view):
        user = request.user
        if not user.is_professor():
            return False
        if getattr(user.professor, 'department'):
            user_pos_departments = self.owner.candidacy_set.values_list(
                'position__department', flat=True)
            if user.professor.department.id in user_pos_departments:
                return True

        user_positions = self.owner.candidacy_set.values_list(
            'position_id', flat=True)
        prof_positions_elector = user.professor.electorparticipation_set. \
            values_list('position_id', flat=True)
        prof_positions_committee = user.professor.committee_duty. \
            values_list('id', flat=True)
        for pid in user_positions:
            if pid in prof_positions_committee or \
                    pid in prof_positions_elector:
                return True

        if self.source == 'position':
            try:
                pos = Position.objects.get(id=self.source_id)
            except Position.DoesNotExist:
                return False
            if getattr(user.professor, 'department') and \
                    user.professor.department == pos.department:
                return True
            if pos.id in prof_positions_elector or \
                    pos.id in prof_positions_committee:
                return True
            if user.id in pos.candidacy_set.values_list(
                    'candidate_id', flat=True):
                return True
        return False

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
        if user.is_assistant() and self.file_kind in [
                'committee_proposal', 'committee_note', 'nomination_act',
                'revocation_decision', 'failed_election_decision',
                'assistant_files', 'electors_set_file', 'committee_set_file']:
            try:
                position = Position.objects.get(id=self.source_id)
            except Position.DoesNotExist:
                logger.error('failed to get Position %r from ApellaFile %r' %
                    (self.source_id, self.id))
                return False
            if assistant_can_edit(position, user):
                return True

        if user.is_manager() and self.is_candidacy_file:
            user_departments = Department.objects.filter(
                institution=user.institutionmanager.institution)
            try:
                candidacy = Candidacy.objects.get(id=self.source_id)
            except Candidacy.DoesNotExist:
                logger.error('failed to get Candidacy %r from file %r' %
                    (self.source_id, self.id))
                return False
            if candidacy.state == 'posted' and \
                    candidacy.position.department in user_departments:
                return True
        if user.is_manager() and self.file_kind == 'cv_professor':
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

        if (self.file_kind == 'id_passport' or
                self.file_kind == 'cv_professor') and \
                is_owner and not is_verified:
            return True
        if self.is_profile_file and is_owner:
            return True
        if self.file_kind in [
                'committee_proposal', 'committee_note', 'nomination_act',
                'revocation_decision', 'failed_election_decision',
                'assistant_files'] \
                and user.is_manager():
            if is_owner:
                return True
            try:
                position = Position.objects.get(id=self.source_id)
            except Position.DoesNotExist:
                logger.error('failed to get Position %r from ApellaFile %r' %
                    (self.source_id, self.id))
                return False
            if user.is_institutionmanager() and self.owner.is_assistant() \
                    and user.institutionmanager.institution == \
                    position.department.institution:
                return True
            if user.is_assistant() and assistant_can_edit(position, user):
                return True
        if self.file_kind == 'attachment_files':
            candidacy = self.attachment_files.all()[0]
            return candidacy.check_resource_state_one_before_electors_meeting(
                row, request, view)
        if self.file_kind == 'self_evaluation_report':
            candidacy = self.self_evaluation_report.all()[0]
            return candidacy.check_resource_state_one_before_electors_meeting(
                row, request, view)
        if self.file_kind == 'statement_file':
            candidacy = self.statement_file.all()[0]
            return candidacy.check_resource_state_five_before_electors_meeting(
                row, request, view)

        return False

    def check_resource_state_public_file(self, row, request, view):
        if self.file_kind == 'registry_set_decision_file':
            return True

    @property
    def is_candidacy_file(self):
        return self.apella_candidacy_cv_files.exists() or \
            self.apella_candidacy_diploma_files.exists() or \
            self.apella_candidacy_publication_files.exists() or \
            self.file_kind in [
                'attachment_files', 'self_evaluation_report', 'statement_file']

    @property
    def is_profile_file(self):
        return self.apella_candidate_cv_files.exists() or \
            self.apella_candidate_diploma_files.exists() or \
            self.apella_candidate_publication_files.exists() or \
            self.apella_professor_cv_files.exists() or \
            self.apella_professor_diploma_files.exists() or \
            self.apella_professor_publication_files.exists()


class Institution(models.Model):
    category = models.CharField(
        choices=common.INSTITUTION_CATEGORIES,
        max_length=30, default='Institution')
    organization = models.URLField(blank=True, max_length=255)
    regulatory_framework = models.URLField(blank=True, max_length=255)
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
    old_code = models.CharField(max_length=255, blank=True, null=True)


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
    cv_url = models.URLField(blank=True, max_length=255)
    cv_professor = models.ForeignKey(
        ApellaFile, blank=True, null=True,
        related_name='professor_cv_file', on_delete=models.SET_NULL)
    fek = models.CharField(max_length=255, blank=True, null=True)
    discipline_text = models.TextField(blank=True)
    discipline_in_fek = models.BooleanField(default=True)

    def check_resource_state_owned(self, row, request, view):
        return request.user.id == self.user.id

    def check_resource_state_participates(self, row, request, view):
        user = request.user
        self_positions_elector = self.electorparticipation_set.values_list(
            'position_id', flat=True)
        self_positions_committee = self.committee_duty.values_list(
            'id', flat=True)
        if user.is_candidate() or user.is_professor():
            user_positions = user.candidacy_set.values_list(
                'position_id', flat=True)
            for pid in user_positions:
                if pid in self_positions_elector \
                        or pid in self_positions_committee:
                    return True
        if user.is_professor():
            prof_elector = user.professor.electorparticipation_set.values_list(
                'position_id', flat=True)
            prof_committee = user.professor.committee_duty.values_list(
                'id', flat=True)
            dep_positions = []
            if user.professor.department:
                dep_positions = Position.objects.filter(
                    department=user.professor.department).values_list(
                        'id', flat=True)
                if dep_positions:
                    for pid in dep_positions:
                        if pid in self_positions_elector or \
                                pid in self_positions_elector:
                            return True
            for pid in prof_committee:
                if pid in self_positions_committee or \
                        pid in self_positions_elector:
                    return True
            for pid in prof_elector:
                if pid in self_positions_committee or \
                        pid in self_positions_elector:
                    return True
        return False

    @property
    def active_elections(self):
        elector_count = 0
        committee_count = 0
        electors_positions = self.electorparticipation_set.values(
            'position__code').annotate(Min('position_id')).values_list(
                'position_id__min', flat=True)
        for p_id in electors_positions:
            if Position.objects.filter(
                    id=p_id,
                    state__in=['electing', 'revoked']). \
                    exists():
                elector_count += 1
        committee_positions = self.committee_duty.values(
            'code').annotate(Min('id')).values_list(
                'id__min', flat=True)
        for p_id in committee_positions:
            if Position.objects.filter(
                    id=p_id,
                    state__in=['electing', 'revoked']). \
                    exists() and p_id not in electors_positions:
                committee_count += 1
        return elector_count + committee_count

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


class UserApplication(models.Model):
    user = models.ForeignKey(ApellaUser)
    department = models.ForeignKey(Department)
    app_type = models.CharField(
        choices=common.APPLICATION_TYPES, max_length=30, default='tenure')
    state = models.CharField(
        choices=common.APPLICATION_STATES, max_length=30, default='pending')
    created_at = models.DateTimeField(default=datetime.utcnow)
    updated_at = models.DateTimeField(default=datetime.utcnow)


    @classmethod
    def check_collection_state_can_create(cls, row, request, view):
        return request.user.is_academic_professor() and \
            request.user.professor.rank == 'Tenured Assistant Professor'

    def check_resource_state_owned(self, row, request, view):
        if not self.user.is_academic_professor() or \
                not self.user.professor.is_verified:
            return False
        if self.user == request.user:
            return True
        if request.user.is_institutionmanager():
            departments = Department.objects.filter(
                institution=request.user.institutionmanager.institution)
            return self.department in departments
        elif request.user.is_assistant():
            return self.department in \
                request.user.institutionmanager.departments.all()
        return False


class Position(models.Model):
    code = models.CharField(max_length=255)
    old_code = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    discipline = models.TextField()
    rank = models.CharField(
        choices=common.POSITION_RANKS, max_length=30, blank=True)
    author = models.ForeignKey(
            InstitutionManager, related_name='authored_positions',
            blank=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    subject_area = models.ForeignKey(SubjectArea, on_delete=models.PROTECT)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    fek = models.URLField(max_length=255, null=True)
    fek_posted_at = models.DateTimeField(null=True)

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
    starts_at = models.DateTimeField(null=True)
    ends_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(default=datetime.utcnow)
    updated_at = models.DateTimeField(default=datetime.utcnow)
    department_dep_number = models.IntegerField()
    electors_meeting_to_set_committee_date = models.DateTimeField(
        blank=True, null=True)
    electors_meeting_date = models.DateTimeField(blank=True, null=True)
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
    nomination_act_fek = models.URLField(blank=True, max_length=255)
    revocation_decision = models.ForeignKey(
        ApellaFile, blank=True, null=True,
        related_name='revocation_decision_files', on_delete=models.SET_NULL)
    failed_election_decision = models.ForeignKey(
        ApellaFile, blank=True, null=True,
        related_name='failed_election_decision_files',
        on_delete=models.SET_NULL)
    assistant_files = models.ManyToManyField(
        ApellaFile, blank=True, related_name='position_assistant_files')
    position_type = models.CharField(
        choices=common.POSITION_TYPES, max_length=30, default='election')
    user_application = models.ForeignKey(
        UserApplication, null=True, on_delete=models.SET_NULL)
    related_positions = models.ManyToManyField('self', blank=True)


    def clean(self, *args, **kwargs):
        if self.is_election_type:
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
        if self.is_election_type:
            return self.state == 'posted' and self.ends_at > datetime.utcnow()
        else:
            return True

    def check_resource_state_revoked(self, row, request, view):
        user = request.user
        revoked = self.state == 'revoked'
        if user.is_institutionmanager() or user.is_helpdeskadmin():
            return revoked
        elif user.is_assistant():
            return revoked and assistant_can_edit(self, user)
        return False

    def check_resource_state_before_open(self, row, request, view):
        user = request.user
        if not self.is_election_type and not self.starts_at:
            before_open = True
        else:
            before_open = self.starts_at > datetime.utcnow()
        if user.is_institutionmanager() or user.is_helpdeskadmin():
            return before_open
        elif user.is_assistant():
            return before_open and assistant_can_edit(self, user)
        return False

    def check_resource_state_after_closed(self, row, request, view):
        user = request.user
        is_posted = self.state == 'posted'
        if not self.ends_at:
            after_closed = False
        else:
            after_closed = self.ends_at < datetime.utcnow() and is_posted
        if user.is_institutionmanager() or user.is_helpdeskadmin():
            return after_closed
        elif user.is_assistant():
            return after_closed and assistant_can_edit(self, user)
        return False

    def check_resource_state_electing(self, row, request, view):
        user = request.user
        is_electing = self.state == 'electing'
        if user.is_institutionmanager() or user.is_helpdeskadmin():
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

    def get_candidates_posted(self):
        """
        Returns a list with  all the candidates (users) whose latest candidacy
        for the position is in state 'posted' and are verified and active.
        """
        c_set = self.candidacy_set.all()
        c_set = c_set.filter(candidate__is_active=True)
        c_set = c_set.filter(
            Q(candidate__candidate__is_verified=True) |
            Q(candidate__professor__is_verified=True))
        updated = c_set.values('candidate').annotate(Max('updated_at')).\
            values('updated_at__max')
        candidacies = c_set.filter(Q(updated_at__in=updated) &
            Q(state='posted'))
        return [x.candidate for x in candidacies]

    def get_users(self):
        """
        Returns a list with all the users that belong to a committee of the
        position, are electors or candidates whose latest candidacy for the
        position is in stated 'posted'.
        All users are verified and active.
        """
        committee = [x.user for x in self.committee.filter(is_verified=True).\
            filter(user__is_active=True)]
        electors = [x.user for x in self.electors.filter(is_verified=True).\
            filter(user__is_active=True)]
        candidates = self.get_candidates_posted()

        return chain(committee, candidates, electors)

    @classmethod
    def check_collection_state_can_create(cls, row, request, view):
        return InstitutionManager.objects.filter(
            user_id=request.user.id,
            manager_role='assistant',
            can_create_positions=True).exists()

    @property
    def is_election_type(self):
        return self.position_type == 'election'

    @property
    def is_tenure_type(self):
        return self.position_type == 'tenure' or \
            self.position_type == 'renewal'


class ElectorParticipation(models.Model):
    professor = models.ForeignKey(Professor)
    position = models.ForeignKey(Position)
    is_regular = models.BooleanField(default=True)
    is_internal = models.BooleanField(default=True)


class Candidacy(CandidateProfile):
    candidate = models.ForeignKey(ApellaUser)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    state = models.CharField(
        choices=common.CANDIDACY_STATES, max_length=30, default='draft')
    others_can_view = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(default=datetime.utcnow)
    updated_at = models.DateTimeField(default=datetime.utcnow)
    code = models.CharField(max_length=255)
    self_evaluation_report = models.ForeignKey(
        ApellaFile, blank=True, null=True,
        related_name='self_evaluation_report', on_delete=models.SET_NULL)
    attachment_files = models.ManyToManyField(
        ApellaFile, blank=True, related_name='attachment_files')
    old_candidacy_id = models.IntegerField(blank=True, null=True)
    statement_file = models.ForeignKey(
        ApellaFile, blank=True, null=True,
        related_name='statement_file', on_delete=models.SET_NULL)

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
            if self.position.electors_meeting_date - datetime.utcnow() > \
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
        return self.position.ends_at < datetime.utcnow() and \
            self.before_electors_meeting(0)

    def check_resource_state_is_dep_candidacy(self, row, request, view):
        if not request.user.is_professor():
            return False
        return getattr(request.user.professor, 'department') and \
            self.position.department == request.user.professor.department


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

    @property
    def members_count(self):
        return self.members.count()

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


class JiraIssue(models.Model):
    code = models.CharField(max_length=255)
    user = models.ForeignKey(ApellaUser, related_name='user')
    reporter = models.ForeignKey(ApellaUser, related_name='reporter')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    state = models.CharField(
        choices=common.JIRA_ISSUE_STATES, max_length=30, default='open')
    issue_type = models.CharField(
        choices=common.JIRA_ISSUE_TYPES, max_length=30, default='complaint')
    resolution = models.CharField(
        choices=common.JIRA_ISSUE_RESOLUTION,
        max_length=30, blank=True, default='')
    created_at = models.DateTimeField(default=datetime.utcnow)
    updated_at = models.DateTimeField(default=datetime.utcnow)
    issue_key = models.CharField(max_length=255, blank=True)


from migration_models import (
    OldApellaUserMigrationData,
    OldApellaFileMigrationData,
    OldApellaPositionMigrationData,
    OldApellaCandidacyFileMigrationData,
    OldApellaCandidacyMigrationData,
    OldApellaInstitutionMigrationData,
    OldApellaCandidateAssistantProfessorMigrationData,
    OldApellaAreaSubscriptions,
)

from serials import Serials
