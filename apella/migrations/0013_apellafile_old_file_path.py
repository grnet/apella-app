# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0012_serials'),
    ]

    operations = [
        migrations.AddField(
            model_name='apellafile',
            name='old_file_path',
            field=models.CharField(default='', max_length=1024),
            preserve_default=False,
        ),
    ]
