# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import apella.validators
import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApellaUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(default=b'2', max_length=1, choices=[['1', 'Institution Manager'], ['2', 'Candidate'], ['3', 'Elector'], ['4', 'Committee'], ['5', 'Assistant']])),
                ('id_passport', models.CharField(max_length=20)),
                ('mobile_phone_number', models.CharField(max_length=30)),
                ('home_phone_number', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ApellaFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_kind', models.CharField(max_length=1, choices=[['CV', 'CV'], ['Diploma', 'Diploma'], ['Publication', 'Publication'], ['Additional file', 'Additional file']])),
                ('file_path', models.CharField(max_length=500)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ApellaUserEl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=300)),
                ('father_name', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ApellaUserEn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=300)),
                ('father_name', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Candidacy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(default=b'2', max_length=1, choices=[['1', 'Draft'], ['2', 'Posted'], ['3', 'Cancelled']])),
                ('others_can_view', models.BooleanField(default=False)),
                ('submitted_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('candidate', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='DepartmentEl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DepartmentEn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(default=b'Institution', max_length=30, choices=[['Institution', 'Institution'], ['Research', 'Research Center']])),
                ('organization', models.URLField(blank=True)),
                ('regulatory_framework', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='InstitutionEl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InstitutionEn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150)),
            ],
            options={
                'abstract': False,
            },
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
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('assistants', models.ManyToManyField(related_name='assistant_duty', to='apella.InstitutionManager', blank=True)),
                ('author', models.ForeignKey(related_name='authored_positions', to='apella.InstitutionManager')),
                ('committee', models.ManyToManyField(related_name='committee_duty', to=settings.AUTH_USER_MODEL, blank=True)),
                ('department', models.ForeignKey(to='apella.Department', on_delete=django.db.models.deletion.PROTECT)),
                ('elected', models.ForeignKey(related_name='elected_positions', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('electors', models.ManyToManyField(related_name='elector_duty', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PositionFiles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False, db_index=True)),
                ('position', models.ForeignKey(related_name='position_files', to='apella.Position')),
                ('position_file', models.ForeignKey(related_name='position_files', to='apella.ApellaFile')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rank', models.CharField(max_length=30, choices=[['Professor', 'Professor'], ['Associate Professor', 'Associate Professor'], ['Assistant Professor', 'Assistant Professor'], ['Research Director', 'Research Director'], ['Principal Researcher', 'Principal Researcher'], ['Affiliated Researcher', 'Affiliated Researcher']])),
                ('is_foreign', models.BooleanField(default=False)),
                ('speaks_greek', models.BooleanField(default=True)),
                ('cv_url', models.URLField(blank=True)),
                ('fek', models.URLField()),
                ('discipline_text', models.CharField(max_length=300)),
                ('discipline_in_fek', models.BooleanField(default=True)),
                ('department', models.ForeignKey(blank=True, to='apella.Department', null=True)),
                ('institution', models.ForeignKey(to='apella.Institution')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Registry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'1', max_length=1, choices=[['1', 'Internal'], ['2', 'External']])),
                ('department', models.ForeignKey(to='apella.Department')),
                ('members', models.ManyToManyField(to='apella.Professor')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolEl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SchoolEn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectAreaEl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubjectAreaEn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubjectEl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubjectEn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserFiles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False, db_index=True)),
                ('apella_file', models.ForeignKey(related_name='user_files', to='apella.ApellaFile')),
                ('apella_user', models.ForeignKey(related_name='user_files', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='subjectarea',
            name='el',
            field=models.ForeignKey(to='apella.SubjectAreaEl'),
        ),
        migrations.AddField(
            model_name='subjectarea',
            name='en',
            field=models.ForeignKey(blank=True, to='apella.SubjectAreaEn', null=True),
        ),
        migrations.AddField(
            model_name='subject',
            name='area',
            field=models.ForeignKey(to='apella.SubjectArea'),
        ),
        migrations.AddField(
            model_name='subject',
            name='el',
            field=models.ForeignKey(to='apella.SubjectEl'),
        ),
        migrations.AddField(
            model_name='subject',
            name='en',
            field=models.ForeignKey(blank=True, to='apella.SubjectEn', null=True),
        ),
        migrations.AddField(
            model_name='school',
            name='el',
            field=models.ForeignKey(to='apella.SchoolEl'),
        ),
        migrations.AddField(
            model_name='school',
            name='en',
            field=models.ForeignKey(blank=True, to='apella.SchoolEn', null=True),
        ),
        migrations.AddField(
            model_name='school',
            name='institution',
            field=models.ForeignKey(to='apella.Institution'),
        ),
        migrations.AddField(
            model_name='position',
            name='subject',
            field=models.ForeignKey(to='apella.Subject', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='position',
            name='subject_area',
            field=models.ForeignKey(to='apella.SubjectArea', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='institution',
            name='el',
            field=models.ForeignKey(to='apella.InstitutionEl'),
        ),
        migrations.AddField(
            model_name='institution',
            name='en',
            field=models.ForeignKey(blank=True, to='apella.InstitutionEn', null=True),
        ),
        migrations.AddField(
            model_name='department',
            name='el',
            field=models.ForeignKey(to='apella.DepartmentEl'),
        ),
        migrations.AddField(
            model_name='department',
            name='en',
            field=models.ForeignKey(blank=True, to='apella.DepartmentEn', null=True),
        ),
        migrations.AddField(
            model_name='department',
            name='institution',
            field=models.ForeignKey(to='apella.Institution'),
        ),
        migrations.AddField(
            model_name='department',
            name='school',
            field=models.ForeignKey(blank=True, to='apella.School', null=True),
        ),
        migrations.AddField(
            model_name='candidacy',
            name='position',
            field=models.ForeignKey(to='apella.Position'),
        ),
        migrations.AddField(
            model_name='apellauser',
            name='el',
            field=models.ForeignKey(to='apella.ApellaUserEl'),
        ),
        migrations.AddField(
            model_name='apellauser',
            name='en',
            field=models.ForeignKey(to='apella.ApellaUserEn'),
        ),
        migrations.AddField(
            model_name='apellauser',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='apellauser',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='registry',
            unique_together=set([('department', 'type')]),
        ),
    ]
