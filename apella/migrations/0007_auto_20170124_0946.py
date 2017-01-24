# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apella.models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0006_auto_20170123_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apellafile',
            name='file_path',
            field=models.FileField(storage=apella.models.OverwriteStorage(), upload_to=apella.models.generate_filename),
        ),
    ]
