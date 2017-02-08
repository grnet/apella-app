# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0021_auto_20170206_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='apellauser',
            name='shibboleth_idp',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='apellauser',
            name='shibboleth_schac_home_organization',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
