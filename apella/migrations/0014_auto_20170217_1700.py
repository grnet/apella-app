# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0013_apellafile_old_file_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apellafile',
            name='file_id',
        ),
        migrations.AlterField(
            model_name='apellafile',
            name='id',
            field=models.BigIntegerField(serialize=False, primary_key=True),
        ),
        migrations.DeleteModel(
            name='ApellaFileId',
        ),
    ]
