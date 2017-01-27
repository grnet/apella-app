# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0011_auto_20170125_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='fek_posted_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='position',
            name='starts_at',
            field=models.DateTimeField(),
        ),
    ]
