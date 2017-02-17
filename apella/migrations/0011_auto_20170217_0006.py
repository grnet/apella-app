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
            name='ApellaFileId',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AlterField(
            model_name='apellafile',
            name='file_content',
            field=models.FileField(max_length=1024, upload_to=apella.models.generate_filename),
        ),
        migrations.AddField(
            model_name='apellafile',
            name='file_id',
            field=models.ForeignKey(default=0, to='apella.ApellaFileId'),
            preserve_default=False,
        ),
    ]
