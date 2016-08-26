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
    electors = models.ManyToManyField(
            ApellaUser, blank=True, related_name='elector_duty')
    committee = models.ManyToManyField(
            ApellaUser, blank=True, related_name='committee_duty')
    elected = models.ForeignKey(
            ApellaUser, blank=True, null=True, related_name='elected_positions')
    state = models.CharField(choices=STATES, max_length=1, default='1')
    starts_at = models.DateField(blank=True, null=True)
    ends_at = models.DateField(blank=True, null=True)


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
    submitted_at = models.DateField(blank=True, null=True)
    state = models.CharField(choices=STATES, max_length=1, default='1')
