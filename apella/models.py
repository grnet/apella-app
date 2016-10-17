from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from apella.validators import before_today_validator, after_today_validator
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


class InstitutionFields(models.Model):
    """
    Abstract model to include fields in different languages
    """
    title = models.CharField(max_length=150, blank=True)

    class Meta:
        abstract = True


class InstitutionEl(InstitutionFields):
    """
    Institution fields in Greek
    """
    pass


class InstitutionEn(InstitutionFields):
    """
    Institution fields in English
    """
    pass


class Institution(models.Model):
    """
    Model for Institutions.
    """
    organization = models.URLField(blank=True)
    regulatory_framework = models.URLField(blank=True)
    el = models.ForeignKey(InstitutionEl, blank=True, null=True)
    en = models.ForeignKey(InstitutionEn, blank=True, null=True)


class InstitutionManager(models.Model):
    """
    Model for institution managers, assistants and manager substitutes
    """
    user = models.ForeignKey(ApellaUser, blank=False, null=False)
    institution = models.ForeignKey(Institution, blank=False, null=False)
    authority = models.CharField(choices=common.AUTHORITIES, max_length=1)
    authority_full_name = models.CharField(max_length=150)
    manager_role = models.CharField(
        choices=common.MANAGER_ROLES, blank=False, max_length=1)


class School(models.Model):
    """
    Model for Schools
    """
    title = models.CharField(max_length=150, blank=False)
    institution = models.ForeignKey(Institution, blank=False, null=False)


class Department(models.Model):
    """
    Model for Departments
    """
    title = models.CharField(max_length=150, blank=False)
    school = models.ForeignKey(School, blank=False, null=False)


class SubjectAreaFields(models.Model):
    """
    Abstract model to include fields in different languages
    """
    title = models.CharField(max_length=200, blank=True)

    class Meta:
        abstract = True


class SubjectAreaEl(SubjectAreaFields):
    pass


class SubjectAreaEn(SubjectAreaFields):
    pass


class SubjectArea(models.Model):
    """
    Model for Subject areas
    """
    el = models.ForeignKey(SubjectAreaEl, blank=True, null=True)
    en = models.ForeignKey(SubjectAreaEn, blank=True, null=True)


class SubjectFields(models.Model):
    """
    Abstract model to include fields in different languages
    """
    title = models.CharField(max_length=200, blank=True)

    class Meta:
        abstract = True


class SubjectEl(SubjectFields):
    pass


class SubjectEn(SubjectFields):
    pass


class Subject(models.Model):
    """
    Model for Subjects
    """
    area = models.ForeignKey(SubjectArea, blank=False, null=False)
    el = models.ForeignKey(SubjectEl, blank=True, null=True)
    en = models.ForeignKey(SubjectEn, blank=True, null=True)


class Position(models.Model):

    """
    Model for positions
    """
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
    created_at = models.DateTimeField(blank=False, default=timezone.now())
    updated_at = models.DateTimeField(blank=False, default=timezone.now())

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(Position, self).save(*args, **kwargs)


class Candidacy(models.Model):

    """
    Model for candidacies
    """
    candidate = models.ForeignKey(ApellaUser, blank=False)
    position = models.ForeignKey(Position, blank=False)
    state = models.CharField(
        choices=common.CANDIDACY_STATES, max_length=1, default='2')
    others_can_view = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(blank=False, default=timezone.now())
    updated_at = models.DateTimeField(blank=False, default=timezone.now())
    # files
    cv = models.CharField(max_length=200)
    diploma = models.CharField(max_length=200)
    publication = models.CharField(max_length=200)
    self_evaluation = models.CharField(max_length=200)
    additional_files = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(Candidacy, self).save(*args, **kwargs)


class Registry(models.Model):
    """
    Model for registries
    """
    class Meta:
        # Each department can have only one internal and one external registry
        unique_together = (("department", "type"),)

    department = models.ForeignKey(Department, blank=False)
    type = models.CharField(
        choices=common.REGISTRY_TYPES, max_length=1, default='1')
    members = models.ManyToManyField(ApellaUser, blank=False, null=False)
