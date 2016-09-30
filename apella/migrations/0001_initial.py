# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import apella.validators
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApellaUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(default=b'2', max_length=1, choices=[['1', 'Institution Manager'], ['2', 'Candidate'], ['3', 'Elector'], ['4', 'Committee'], ['5', 'Assistant']])),
                ('father_name', models.CharField(max_length=50)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Candidacy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(default=b'2', max_length=1, choices=[['1', 'Draft'], ['2', 'Posted'], ['3', 'Cancelled']])),
                ('others_can_view', models.BooleanField(default=False)),
                ('submitted_at', models.DateTimeField(default=datetime.datetime(2016, 9, 30, 8, 5, 46, 734724))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2016, 9, 30, 8, 5, 46, 734748))),
                ('cv', models.CharField(max_length=200)),
                ('diploma', models.CharField(max_length=200)),
                ('publication', models.CharField(max_length=200)),
                ('self_evaluation', models.CharField(max_length=200)),
                ('additional_files', models.CharField(max_length=200)),
                ('candidate', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150)),
                ('organization', models.URLField(blank=True)),
                ('regulatory_framework', models.URLField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstitutionManager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('authority', models.CharField(max_length=1, choices=[['1', 'Dean'], ['2', 'President']])),
                ('authority_full_name', models.CharField(max_length=150)),
                ('manager_role', models.CharField(max_length=1, choices=[['1', 'Manager'], ['2', 'Assistant'], ['3', 'Substitute']])),
                ('institution', models.ForeignKey(to='apella.Institution')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=300)),
                ('discipline', models.CharField(max_length=300)),
                ('fek', models.URLField()),
                ('fek_posted_at', models.DateTimeField(validators=[apella.validators.before_today_validator])),
                ('state', models.CharField(default=b'2', max_length=1, choices=[['1', 'Draft'], ['2', 'Posted'], ['3', 'Electing'], ['4', 'Successful'], ['5', 'Failed']])),
                ('starts_at', models.DateTimeField(validators=[apella.validators.after_today_validator])),
                ('ends_at', models.DateTimeField()),
                ('created_at', models.DateTimeField(default=datetime.datetime(2016, 9, 30, 8, 5, 46, 732189))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2016, 9, 30, 8, 5, 46, 732215))),
                ('assistants', models.ManyToManyField(related_name='assistant_duty', to='apella.InstitutionManager', blank=True)),
                ('author', models.ForeignKey(related_name='authored_positions', to='apella.InstitutionManager')),
                ('committee', models.ManyToManyField(related_name='committee_duty', to=settings.AUTH_USER_MODEL, blank=True)),
                ('department', models.ForeignKey(to='apella.Department')),
                ('elected', models.ForeignKey(related_name='elected_positions', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('electors', models.ManyToManyField(related_name='elector_duty', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Registry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'1', max_length=1, choices=[['1', 'Internal'], ['2', 'External']])),
                ('department', models.ForeignKey(to='apella.Department')),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150)),
                ('institution', models.ForeignKey(to='apella.Institution')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubjectArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='subject',
            name='area',
            field=models.ForeignKey(to='apella.SubjectArea'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='registry',
            unique_together=set([('department', 'type')]),
        ),
        migrations.AddField(
            model_name='position',
            name='subject',
            field=models.ForeignKey(to='apella.Subject'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='position',
            name='subject_area',
            field=models.ForeignKey(to='apella.SubjectArea'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='department',
            name='school',
            field=models.ForeignKey(to='apella.School'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='candidacy',
            name='position',
            field=models.ForeignKey(to='apella.Position'),
            preserve_default=True,
        ),
    ]
