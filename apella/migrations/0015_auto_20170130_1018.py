# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0014_auto_20170129_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='oldapellacandidacymigrationdata',
            name='created_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='oldapellacandidacymigrationdata',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
    ]
