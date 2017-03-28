# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0020_oldapellaareasubscriptions_departments_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserApplication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_type', models.CharField(default=b'tenure', max_length=30, choices=[['tenure', 'Tenure'], ['renewal', 'Renewal']])),
                ('state', models.CharField(default=b'pending', max_length=30, choices=[['pending', 'Pending'], ['approved', 'Approved'], ['rejected', 'Rejected']])),
                ('created_at', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
