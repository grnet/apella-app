# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0021_auto_20170411_1144'),
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
        migrations.AddField(
            model_name='position',
            name='position_type',
            field=models.CharField(default=b'election', max_length=30, choices=[['election', 'Election'], ['tenure', 'Tenure'], ['renewal', 'Renewal']]),
        ),
        migrations.AlterField(
            model_name='position',
            name='ends_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='fek',
            field=models.URLField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='fek_posted_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='starts_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='position',
            name='user_application',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='apella.UserApplication', null=True),
        ),
    ]
