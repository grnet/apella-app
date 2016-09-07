#! /usr/bin/env python
import os
from StringIO import StringIO

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apella_app.settings")

import django
from django.core import management
from django.core.management.commands import *
from apella.management.commands import *

django.setup()

management.call_command('user-add', 'manager', '12345', role='1')
management.call_command('user-add', 'candidate', '12345', role='2')
management.call_command('user-add', 'elector', '12345', role='3')
management.call_command('user-add', 'committee', '12345', role='4')

i_out = StringIO()
management.call_command('institution-add', 'Test institution', stdout=i_out)
print(i_out.getvalue())
ints = [int(s) for s in i_out.getvalue().split() if s.isdigit()]
institution_id = ints[0]

p_out = StringIO()
management.call_command(
    'position-add', 'New position', 'manager', institution_id, stdout=p_out)
print(p_out.getvalue())
ints = [int(s) for s in p_out.getvalue().split() if s.isdigit()]
position_id = ints[0]

management.call_command('position-post', position_id)

c_out = StringIO()
management.call_command('candidacy-add', position_id, 'candidate', stdout=c_out)
print(c_out.getvalue())
ints2 = [int(s) for s in c_out.getvalue().split() if s.isdigit()]
candidacy_id = ints2[0]

management.call_command('candidacy-post', candidacy_id)

management.call_command('position-modify', position_id, electors='elector')
management.call_command('position-modify', position_id, committee='committee')

management.call_command('position-modify', position_id, elected='candidate')

