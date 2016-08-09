from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext as _


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
    id_passport = models.CharField(max_length=20, blank=False)
    phone = models.CharField(max_length=20, blank=False)
