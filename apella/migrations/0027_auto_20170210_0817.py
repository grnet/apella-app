# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0026_auto_20170209_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oldapellacandidacymigrationdata',
            name='withdrawn_at',
            field=models.TextField(null=True),
        ),
    ]
