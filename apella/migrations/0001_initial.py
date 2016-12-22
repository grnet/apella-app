# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apella.validators
import apella.models
import django.contrib.auth.models
import django.db.models.deletion
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
                ('username', models.CharField(help_text=b'Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True, error_messages={b'unique': b'A user with that username already exists.'}, validators=[django.core.validators.RegexValidator(b'^[\\w.@+-]+$', b'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', b'invalid')])),
                ('email', models.EmailField(unique=True, max_length=254, error_messages={b'unique': b'A user with that email already exists.'})),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('email_verified', models.BooleanField(default=False)),
                ('email_verified_at', models.DateTimeField(default=None, null=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('id_passport', models.CharField(max_length=20, blank=True)),
                ('mobile_phone_number', models.CharField(max_length=30, blank=True)),
                ('home_phone_number', models.CharField(max_length=30, blank=True)),
                ('role', models.CharField(default=b'candidate', max_length=20, choices=[['institutionmanager', 'Institution Manager'], ['candidate', 'Candidate'], ['professor', 'Professor'], ['helpdeskadmin', 'Helpdesk Admin'], ['helpdeskuser', 'Helpdesk User'], ['assistant', 'Assistant']])),
                ('shibboleth_id', models.CharField(default=None, max_length=255, unique=True, null=True)),
                ('shibboleth_id_legacy', models.CharField(default=None, max_length=255, null=True)),
                ('shibboleth_registration_key', models.CharField(default=None, max_length=255, null=True)),
                ('shibboleth_migration_key', models.CharField(default=None, max_length=255, null=True)),
            ],
            options={
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
                ('source', models.CharField(max_length=30, choices=[['profile', 'Profile'], ['candidacy', 'Candidacy'], ['position', 'Position'], ['other', 'Other']])),
                ('source_id', models.IntegerField()),
                ('file_kind', models.CharField(max_length=40, choices=[['CV', 'CV'], ['Diploma', 'Diploma'], ['Publication', 'Publication'], ['Additional file', 'Additional file']])),
                ('file_path', models.FileField(upload_to=apella.models.generate_filename)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Candidacy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(default=b'posted', max_length=30, choices=[['posted', 'Posted'], ['cancelled', 'Cancelled']])),
                ('others_can_view', models.BooleanField(default=False)),
                ('submitted_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('code', models.CharField(max_length=200)),
                ('candidate', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=False)),
                ('activated_at', models.DateTimeField(null=True, blank=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('verified_at', models.DateTimeField(null=True, blank=True)),
                ('is_rejected', models.BooleanField(default=False)),
                ('rejected_reason', models.TextField(null=True, blank=True)),
                ('cv', models.ForeignKey(blank=True, to='apella.ApellaFile', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dep_number', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ElectorParticipation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_regular', models.BooleanField(default=True)),
            ],
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
            name='InstitutionManager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=False)),
                ('activated_at', models.DateTimeField(null=True, blank=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('verified_at', models.DateTimeField(null=True, blank=True)),
                ('is_rejected', models.BooleanField(default=False)),
                ('rejected_reason', models.TextField(null=True, blank=True)),
                ('authority', models.CharField(max_length=1, choices=[['1', 'Dean'], ['2', 'President']])),
                ('authority_full_name', models.CharField(max_length=150)),
                ('manager_role', models.CharField(max_length=20, choices=[['institutionmanager', 'Manager'], ['assistant', 'Assistant']])),
                ('sub_email', models.EmailField(max_length=254, null=True, blank=True)),
                ('sub_mobile_phone_number', models.CharField(max_length=30, null=True, blank=True)),
                ('sub_home_phone_number', models.CharField(max_length=30, null=True, blank=True)),
                ('can_create_registries', models.BooleanField(default=False)),
                ('can_create_positions', models.BooleanField(default=False)),
                ('institution', models.ForeignKey(to='apella.Institution', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MultiLangFields',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('el', models.CharField(max_length=500, null=True, blank=True)),
                ('en', models.CharField(max_length=500, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=300)),
                ('discipline', models.CharField(max_length=300)),
                ('fek', models.URLField()),
                ('fek_posted_at', models.DateTimeField(validators=[apella.validators.before_today_validator])),
                ('state', models.CharField(default=b'posted', max_length=30, choices=[['draft', 'Draft'], ['posted', 'Posted'], ['electing', 'Electing'], ['successful', 'Successful'], ['failed', 'Failed'], ['cancelled', 'Cancelled'], ['revoked', 'Revoked']])),
                ('starts_at', models.DateTimeField(validators=[apella.validators.after_today_validator])),
                ('ends_at', models.DateTimeField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('department_dep_number', models.IntegerField()),
                ('assistants', models.ManyToManyField(related_name='assistant_duty', to='apella.InstitutionManager', blank=True)),
                ('author', models.ForeignKey(related_name='authored_positions', blank=True, to='apella.InstitutionManager')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=False)),
                ('activated_at', models.DateTimeField(null=True, blank=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('verified_at', models.DateTimeField(null=True, blank=True)),
                ('is_rejected', models.BooleanField(default=False)),
                ('rejected_reason', models.TextField(null=True, blank=True)),
                ('rank', models.CharField(max_length=30, choices=[['Professor', 'Professor'], ['Associate Professor', 'Associate Professor'], ['Assistant Professor', 'Assistant Professor'], ['Research Director', 'Research Director'], ['Principal Researcher', 'Principal Researcher'], ['Affiliated Researcher', 'Affiliated Researcher']])),
                ('is_foreign', models.BooleanField(default=False)),
                ('speaks_greek', models.BooleanField(default=True)),
                ('cv_url', models.URLField(blank=True)),
                ('fek', models.URLField()),
                ('discipline_text', models.CharField(max_length=300, blank=True)),
                ('discipline_in_fek', models.BooleanField(default=True)),
                ('cv', models.ForeignKey(blank=True, to='apella.ApellaFile', null=True)),
                ('department', models.ForeignKey(blank=True, to='apella.Department', null=True)),
                ('institution', models.ForeignKey(to='apella.Institution', on_delete=django.db.models.deletion.PROTECT)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProfessorRank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rank', models.ForeignKey(to='apella.MultiLangFields')),
            ],
        ),
        migrations.CreateModel(
            name='RegistrationToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(unique=True, max_length=255, blank=True)),
                ('identifier', models.CharField(max_length=255, blank=True)),
                ('data', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Registry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'1', max_length=1, choices=[['1', 'Internal'], ['2', 'External']])),
                ('department', models.ForeignKey(to='apella.Department', on_delete=django.db.models.deletion.PROTECT)),
                ('members', models.ManyToManyField(to='apella.Professor')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('institution', models.ForeignKey(to='apella.Institution', on_delete=django.db.models.deletion.PROTECT)),
                ('title', models.ForeignKey(to='apella.MultiLangFields')),
            ],
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
                ('title', models.ForeignKey(to='apella.MultiLangFields')),
            ],
        ),
        migrations.CreateModel(
            name='UserInterest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('area', models.ManyToManyField(to='apella.SubjectArea', blank=True)),
                ('department', models.ManyToManyField(to='apella.Department', blank=True)),
                ('institution', models.ManyToManyField(to='apella.Institution', blank=True)),
                ('subject', models.ManyToManyField(to='apella.Subject', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='subject',
            name='area',
            field=models.ForeignKey(to='apella.SubjectArea'),
        ),
        migrations.AddField(
            model_name='subject',
            name='title',
            field=models.ForeignKey(to='apella.MultiLangFields'),
        ),
        migrations.AddField(
            model_name='position',
            name='committee',
            field=models.ManyToManyField(related_name='committee_duty', to='apella.Professor', blank=True),
        ),
        migrations.AddField(
            model_name='position',
            name='department',
            field=models.ForeignKey(to='apella.Department', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='position',
            name='elected',
            field=models.ForeignKey(related_name='elected_positions', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='position',
            name='electors',
            field=models.ManyToManyField(to='apella.Professor', through='apella.ElectorParticipation', blank=True),
        ),
        migrations.AddField(
            model_name='position',
            name='ranks',
            field=models.ManyToManyField(to='apella.ProfessorRank', blank=True),
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
            model_name='institutionmanager',
            name='sub_father_name',
            field=models.ForeignKey(related_name='sub_father_name', blank=True, to='apella.MultiLangFields', null=True),
        ),
        migrations.AddField(
            model_name='institutionmanager',
            name='sub_first_name',
            field=models.ForeignKey(related_name='sub_first_name', blank=True, to='apella.MultiLangFields', null=True),
        ),
        migrations.AddField(
            model_name='institutionmanager',
            name='sub_last_name',
            field=models.ForeignKey(related_name='sub_last_name', blank=True, to='apella.MultiLangFields', null=True),
        ),
        migrations.AddField(
            model_name='institutionmanager',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='institution',
            name='title',
            field=models.ForeignKey(to='apella.MultiLangFields'),
        ),
        migrations.AddField(
            model_name='electorparticipation',
            name='position',
            field=models.ForeignKey(to='apella.Position'),
        ),
        migrations.AddField(
            model_name='electorparticipation',
            name='professor',
            field=models.ForeignKey(to='apella.Professor'),
        ),
        migrations.AddField(
            model_name='department',
            name='institution',
            field=models.ForeignKey(to='apella.Institution', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='department',
            name='school',
            field=models.ForeignKey(blank=True, to='apella.School', null=True),
        ),
        migrations.AddField(
            model_name='department',
            name='title',
            field=models.ForeignKey(to='apella.MultiLangFields'),
        ),
        migrations.AddField(
            model_name='candidacy',
            name='position',
            field=models.ForeignKey(to='apella.Position', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='apellauser',
            name='father_name',
            field=models.ForeignKey(related_name='father_name', blank=True, to='apella.MultiLangFields', null=True),
        ),
        migrations.AddField(
            model_name='apellauser',
            name='first_name',
            field=models.ForeignKey(related_name='first_name', to='apella.MultiLangFields'),
        ),
        migrations.AddField(
            model_name='apellauser',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='apellauser',
            name='last_name',
            field=models.ForeignKey(related_name='last_name', to='apella.MultiLangFields'),
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
