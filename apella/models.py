from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from apella.validators import before_today_validator, after_today_validator
from apella import common


class ApellaUser(AbstractUser):

    """
    Model for users of `Apella`.

    It actually inherits from `AbstractUser` class of
    `django.contib.auth.models` which define common fields such as first name,
    last name, email, etc
    """
    role = models.CharField(
        choices=common.USER_ROLES, max_length=1, default='2')


class Institution(models.Model):
    """
    Model for Institutions
    """
    title = models.CharField(max_length=150, blank=False)
    organization = models.URLField(blank=True)
    regulatory_framework = models.URLField(blank=True)


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


class SubjectArea(models.Model):
    """
    Model for Subject areas
    """
    title = models.CharField(max_length=200, blank=False, null=False)


class Subject(models.Model):
    """
    Model for Subjects
    """
    title = models.CharField(max_length=200, blank=False, null=False)
    area = models.ForeignKey(SubjectArea, blank=False, null=False)


class Position(models.Model):

    """
    Model for positions
    """
    title = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=300, blank=False, null=False)
    discipline = models.CharField(max_length=300, blank=False, null=False)
    author = models.ForeignKey(
            ApellaUser, blank=False, related_name='authored_positions')
    department = models.ForeignKey(Department, blank=False, null=False)
    subject_area = models.ForeignKey(SubjectArea, blank=False, null=False)
    subject = models.ForeignKey(Subject, blank=False, null=False)
    fek = models.URLField(blank=False, null=False)
    fek_posted_at = models.DateTimeField(
        blank=False, null=False, validators=[before_today_validator])

    assistants = models.ManyToManyField(
            ApellaUser, blank=True, related_name='assistant_duty')
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
