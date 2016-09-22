from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from apella.validators import before_today_validator, after_today_validator


class ApellaUser(AbstractUser):

    """
    Model for users of `Apella`.

    It actually inherits from `AbstractUser` class of
    `django.contib.auth.models` which define common fields such as first name,
    last name, email, etc
    """
    ROLES = (
        ('1', 'Insitution Manager'),
        ('2', 'Candidate'),
        ('3', 'Elector'),
        ('4', 'Committee'),
        ('5', 'Assistant'),
    )
    role = models.CharField(choices=ROLES, max_length=1, default='2')
    files = models.CharField(max_length=200)


class Institution(models.Model):
    """
    Model for Institutions
    """
    title = models.CharField(max_length=150, blank=False)


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
    STATES = (
        ('1', 'Draft'),
        ('2', 'Posted'),
        ('3', 'Electing'),
        ('4', 'Successful'),
        ('5', 'Failed')
    )

    title = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=300, blank=False, null=False)
    discipline = models.CharField(max_length=300, blank=False, null=False)
    author = models.ForeignKey(
            ApellaUser, blank=False, related_name='authored_positions')
    department = models.ForeignKey(Department, blank=False, null=False)
    subject_area = models.ForeignKey(SubjectArea, blank=False, null=False)
    subject = models.ForeignKey(Subject, blank=False, null=False)
    fek = models.URLField(blank=False, null=False)
    fek_posted_at = models.DateField(
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

    state = models.CharField(choices=STATES, max_length=1, default='2')
    starts_at = models.DateTimeField(
        blank=False, null=False, validators=[after_today_validator])
    ends_at = models.DateTimeField(blank=False, null=False)


class Candidacy(models.Model):

    """
    Model for candidacies
    """
    STATES = (
        ('1', 'Draft'),
        ('2', 'Posted'),
        ('3', 'Cancelled')
    )

    candidate = models.ForeignKey(ApellaUser, blank=False)
    position = models.ForeignKey(Position, blank=False)
    submitted_at = models.DateTimeField(blank=True, null=True)
    state = models.CharField(choices=STATES, max_length=1, default='2')
    files = models.CharField(max_length=200)


class Registry(models.Model):
    """
    Model for registries
    """
    class Meta:
        # Each department can have only one internal and one external registry
        unique_together = (("department", "type"),)

    TYPES = (
        ('1', 'Internal'),
        ('2', 'External')
    )

    department = models.ForeignKey(Department, blank=False)
    type = models.CharField(choices=TYPES, max_length=1, default='1')
    members = models.ManyToManyField(ApellaUser, blank=False, null=False)
