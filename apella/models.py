from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext as _

# Users related models

class ProfessorProfile(models.Model):
    """
    Abstract model with common Professor (domestic and foreign) fields
    """

    RANKS = (
        ('A', _('Professor')),
        ('B', _('Assistant')),
    )
    rank= models.CharField(
        max_length=1,
        choices=RANKS,
        default='B',
    )
    no_cv_url = models.BooleanField()
    cv_url = models.URLField(blank=True)
    cv = models.FileField(upload_to='uploads/')
    subject = models.CharField(max_length=255, blank=True)
    has_accepted_terms = models.BooleanField()
    class Meta:
        abstract = True


class UserProfile(AbstractUser):

    """
    Model for users of `Apella`.

    It actually inherits from `AbstractUser` class of
    `django.contib.auth.models` which define common fields such as first name,
    last name, email, etc
    """

    father_name = models.CharField(max_length=30, blank=False)
    first_name_latin = models.CharField(max_length=30, blank=True)
    last_name_latin = models.CharField(max_length=30, blank=True)
    father_name_latin = models.CharField(max_length=30, blank=True)
    id_passport = models.CharField(max_length=20, blank=False,
            help_text=_('ID or passport'))
    phone = models.CharField(max_length=20, blank=False)


class DomesticProfessor(ProfessorProfile, UserProfile):
    #institute = models.ForeignKey('Institute')
    institute = models.CharField(max_length=30, blank=False)
    fek = models.CharField(max_length=255, blank=False)
    fek_file = models.FileField(upload_to='uploads/')
    no_fek_subject = models.BooleanField()
    fek_subject = models.CharField(max_length=255, blank=True)

class ForeignProfessor(ProfessorProfile, UserProfile):
    pass


# Non users related models
