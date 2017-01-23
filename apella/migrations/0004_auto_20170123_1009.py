# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0003_oldapellausermigrationdata_permanent_auth_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidacy',
            name='code',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='position',
            name='code',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='position',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='position',
            name='discipline',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='position',
            name='old_code',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='position',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
