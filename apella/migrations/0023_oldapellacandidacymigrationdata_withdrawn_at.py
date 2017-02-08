# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0022_auto_20170208_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='oldapellacandidacymigrationdata',
            name='withdrawn_at',
            field=models.DateTimeField(null=True),
        ),
    ]
