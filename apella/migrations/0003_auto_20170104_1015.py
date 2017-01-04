# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0002_auto_20170103_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='apellauser',
            name='login_method',
            field=models.CharField(default=b'password', max_length=20),
        ),
        migrations.AlterField(
            model_name='apellafile',
            name='file_kind',
            field=models.CharField(max_length=40, choices=[['CV', 'CV'], ['Diploma', 'Diploma'], ['Publication', 'Publication'], ['Additional file', 'Additional file']]),
        ),
    ]
