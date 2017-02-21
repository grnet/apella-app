# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apella.models


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0010_auto_20170216_1614'),
    ]

    operations = [
        migrations.CreateModel(
            name='Serials',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('value', models.BigIntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='apellafile',
            name='old_file_path',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='apellafile',
            name='file_content',
            field=models.FileField(max_length=1024, upload_to=apella.models.generate_filename),
        ),
        migrations.AlterField(
            model_name='apellafile',
            name='id',
            field=models.BigIntegerField(serialize=False, primary_key=True),
        ),
    ]
