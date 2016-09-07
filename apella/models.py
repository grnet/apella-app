from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


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
        ('4', 'Committee')
    )
    role = models.CharField(choices=ROLES, max_length=1, default='2')

class Institution(models.Model):
    """
    Model for Institutions
    """
    title = models.CharField(max_length=150, blank=False)

class Department(models.Model):
    """
    Model for Institutions
    """
    title = models.CharField(max_length=150, blank=False)
    institution = models.ForeignKey(Institution, blank=False, null=False)

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

    title = models.CharField(max_length=50, blank=False)
    author = models.ForeignKey(
            ApellaUser, blank=False, related_name='authored_positions')
    department = models.ForeignKey(Department, blank=False, null=False)
    electors = models.ManyToManyField(
            ApellaUser, blank=True, related_name='elector_duty')
    committee = models.ManyToManyField(
            ApellaUser, blank=True, related_name='committee_duty')
    elected = models.ForeignKey(
            ApellaUser, blank=True, null=True, related_name='elected_positions')
    state = models.CharField(choices=STATES, max_length=1, default='1')
    starts_at = models.DateTimeField(blank=True, null=True)
    ends_at = models.DateTimeField(blank=True, null=True)


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
    state = models.CharField(choices=STATES, max_length=1, default='1')

class Registry(models.Model):
    """
    Model for registries
    """
    TYPES = (
        ('1', 'Internal'),
        ('2', 'External')
    )

    department = models.CharField(max_length=200, blank=False)
    type = models.CharField(choices=TYPES, max_length=1, default='1')
    members = models.ManyToManyField(ApellaUser, blank=False, null=False)
