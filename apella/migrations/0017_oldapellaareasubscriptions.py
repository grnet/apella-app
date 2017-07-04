# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0016_electorparticipation_is_internal'),
    ]

    operations = [
        migrations.CreateModel(
            name='OldApellaAreaSubscriptions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.TextField()),
                ('version', models.TextField()),
                ('sector_id', models.TextField()),
                ('area_id', models.TextField()),
                ('subject_id', models.TextField()),
                ('area_name', models.TextField()),
                ('subject_name', models.TextField()),
                ('locale', models.TextField()),
            ],
        ),
    ]
