# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0017_institutionmanager_is_secretary'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='has_shibboleth',
            field=models.BooleanField(default=False),
        ),
    ]
