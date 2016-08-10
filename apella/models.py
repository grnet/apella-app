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
    rank = models.CharField(
        max_length=1,
        choices=RANKS,
        default='B',
    )
    no_cv_url = models.BooleanField()
    cv_url = models.URLField(blank=True)
    cv = models.FileField(upload_to='uploads/', blank=True)
    discipline = models.CharField(max_length=255, blank=True)
    has_accepted_terms = models.BooleanField(default=False)
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


class DomesticProfessor(ProfessorProfile):
    user = models.OneToOneField(UserProfile)
    #institution = models.ForeignKey('Institution')
    institution = models.CharField(max_length=30, blank=False)
    fek = models.CharField(max_length=255, blank=False)
    fek_file = models.FileField(upload_to='uploads/',blank=True)
    no_fek_subject = models.BooleanField()
    fek_subject = models.CharField(max_length=255, blank=True)

class ForeignProfessor(ProfessorProfile):
    user = models.OneToOneField(UserProfile)
    COUNTRIES = (
        ('GR', _('Greece')),
        ('FR', _('France')),
    )
    country= models.CharField(
        max_length=2,
        choices=COUNTRIES,
        default='FR',
    )
    speaks_greek = models.BooleanField(default=False)

class InstitutionAdmin(models.Model):
    user = models.OneToOneField(UserProfile)
    #institution = models.ForeignKey('Institution')
    institution = models.CharField(max_length=30, blank=False)
    AUTHORITIES = (
        ('1', _('Dean')),
        ('2', _('President')),
    )
    ROLES = (
        ('0', _('Admin')),
        ('1', _('Substitute')),
        ('2', _('Helper')),
    )
    authority = models.CharField(
        max_length=1,
        choices=AUTHORITIES,
        default='1',
    )
    authority_name = models.CharField(max_length=255, blank=False)
    role = models.CharField(
        max_length=1,
        choices=ROLES,
        default='1'
    )

class ApellaAdmin(models.Model):
    user = models.OneToOneField(UserProfile)
    ROLES = (
        ('0', _('Superadmin')),
        ('1', _('Helpdesk')),
        ('2', _('Ministry')),
    )

    role = models.CharField(
        max_length=1,
        choices=ROLES,
        default='1'
    )


# Non users related models
