# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0011_auto_20170220_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oldapellacandidacyfilemigrationdata',
            name='candidacy_serial',
            field=models.TextField(db_index=True),
        ),
        migrations.AlterField(
            model_name='oldapellacandidacymigrationdata',
            name='candidate_user_id',
            field=models.TextField(db_index=True),
        ),
        migrations.AlterField(
            model_name='oldapellacandidacymigrationdata',
            name='position_serial',
            field=models.TextField(db_index=True),
        ),
        migrations.AlterField(
            model_name='oldapellafilemigrationdata',
            name='user_id',
            field=models.TextField(db_index=True),
        ),
    ]
