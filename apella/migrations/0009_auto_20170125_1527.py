# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0008_auto_20170125_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apellafile',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
    ]
