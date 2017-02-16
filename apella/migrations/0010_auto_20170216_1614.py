# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0009_subject_old_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apellafile',
            old_name='file_path',
            new_name='file_content',
        ),
        migrations.AddField(
            model_name='apellafile',
            name='file_name',
            field=models.CharField(default='apella-download', max_length=1024),
            preserve_default=False,
        ),
    ]
