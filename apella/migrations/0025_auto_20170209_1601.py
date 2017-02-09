# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0024_auto_20170209_1014'),
    ]

    operations = [
        migrations.RenameField(
            model_name='oldapellacandidacymigrationdata',
            old_name='created_at',
            new_name='submitted_at',
        ),
        migrations.RemoveField(
            model_name='oldapellacandidacymigrationdata',
            name='updated_at',
        ),
    ]
