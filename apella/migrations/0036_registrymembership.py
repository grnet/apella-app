# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0035_auto_20180202_1017'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistryMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('professor', models.ForeignKey(to='apella.Professor', on_delete=django.db.models.deletion.PROTECT)),
                ('registry', models.ForeignKey(to='apella.Registry', on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
    ]
