# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0025_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='JiraIssue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('state', models.CharField(default=b'open', max_length=30, choices=[['open', 'Open'], ['closed', 'Closed'], ['in_progress', 'In Progress'], ['reopened', 'Reopened'], ['resolved', 'Resolved']])),
                ('issue_type', models.CharField(default=b'complaint', max_length=30, choices=[['complaint', 'Complaint'], ['error', 'Error'], ['login', 'Login'], ['general_information', 'General Information'], ['account_modification', 'Account Modification'], ['registration', 'Registration']])),
                ('resolution', models.CharField(default=b'fixed', max_length=30, choices=[['fixed', 'Fixed'], ['wont_fix', "Won't Fix"], ['duplicate', 'Duplicate'], ['incomplete', 'Incomplete'], ['cannot_reproduce', 'Cannot Reproduce'], ['fixed_workaround', 'Fixed Workaround']])),
                ('created_at', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('reporter', models.ForeignKey(related_name='reporter', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
