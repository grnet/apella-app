# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0023_oldapellacandidacymigrationdata_withdrawn_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apellauser',
            name='id_passport',
            field=models.CharField(max_length=30, blank=True),
        ),
    ]
