# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0020_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='idp',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='institution',
            name='schac_home_organization',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
