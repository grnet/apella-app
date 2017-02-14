# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0005_auto_20170214_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apellauser',
            name='username',
            field=models.CharField(help_text=b'Required. 255 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=255, unique=True, error_messages={b'unique': b'A user with that username already exists.'}, validators=[django.core.validators.RegexValidator(b'^[\\w.@+-]+$', b'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', b'invalid')]),
        ),
    ]
