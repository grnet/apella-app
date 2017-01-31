# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0018_institution_has_shibboleth'),
    ]

    operations = [
        migrations.CreateModel(
            name='OldApellaCandidateAssistantProfessorMigrationData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.TextField()),
                ('account_status', models.TextField()),
                ('surname_el', models.TextField()),
                ('name_el', models.TextField()),
                ('fathername_el', models.TextField()),
                ('email', models.TextField()),
                ('institution', models.TextField()),
                ('department', models.TextField()),
                ('rank', models.TextField()),
            ],
        ),
    ]
