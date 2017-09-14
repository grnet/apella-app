# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0029_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='jiraissue',
            name='issue_call',
            field=models.CharField(default=b'incoming', max_length=30, choices=[['incoming', 'Incoming'], ['outgoing', 'Outgoing']]),
        ),
    ]
