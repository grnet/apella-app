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


class Position(models.Model):

    """
    Model for positions
    """
    STATES = (
        ('1', 'Draft'),
        ('2', 'Posted'),
        ('3', 'Electing'),
        ('4', 'Closed'),
        ('5', 'Cancelled')
    )

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, blank=False)
    author = models.ForeignKey(ApellaUser, blank=False, related_name='author')
    electors = models.ManyToManyField(ApellaUser, blank=True,
            related_name='electors')
    committee = models.ManyToManyField(ApellaUser, blank=True,
            related_name='committee')
    elected = models.ForeignKey(ApellaUser, blank=True, related_name='elected')
    state = models.CharField(choices=STATES, max_length=1, default='1')


class Candidacy(models.Model):

    """
    Model for candidacies
    """
    STATES = (
        ('1', 'Active'),
        ('2', 'Cancelled')
    )

    candidate = models.ForeignKey(ApellaUser, blank=False)
    position = models.ForeignKey(Position, blank=False)
    state = models.CharField(choices=STATES, max_length=1, default='1')

