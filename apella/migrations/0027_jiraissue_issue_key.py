# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0026_jiraissue'),
    ]

    operations = [
        migrations.AddField(
            model_name='jiraissue',
            name='issue_key',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
