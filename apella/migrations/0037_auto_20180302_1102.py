# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

STEP = 500

def migrate_registries(apps, schema_editor):
    Registry = apps.get_model('apella', 'Registry')
    RegistryMembership = apps.get_model('apella', 'RegistryMembership')

    for r in Registry.objects.all():
        total = r.members.count()
        begin = 0
        memberships = []
        while begin < total:
            end = min(begin + STEP, total)
            for p in r.members.order_by('user_id')[begin:end]:
                memberships.append(RegistryMembership(
                                        registry=r,
                                        professor=p))
            RegistryMembership.objects.bulk_create(memberships)
            memberships = []
            begin = end


class Migration(migrations.Migration):

    dependencies = [
        ('apella', '0036_registrymembership'),
    ]

    operations = [
            migrations.RunPython(migrate_registries)
    ]
