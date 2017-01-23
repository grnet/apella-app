# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0005_oldapellausermigrationdata_role_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oldapellausermigrationdata',
            name='permanent_auth_token',
            field=models.TextField(null=True),
        ),
    ]
