
"""
Role, Resource, Fields, Operation, State, Spec number
"""

from tabmatch import Tabmatch

tb = Tabmatch(('role', 'resource', 'field', 'action', 'state', 'section'))
Row = tb.Row


PERMISSIONS = [
    Row('institutionmanager',    'institutions', '*', 'list', '*', '4.3.22'),
    Row('professor',             'institutions', '*', 'list', '*', '1.3.15'),
    Row('candidate',             'institutions', '*', 'list', '*', '3.3.10'),
    Row('helpdeskadmin',         'institutions', '*', 'list', '*', '5.8'),
    Row('helpdeskuser',          'institutions', '*', 'list', '*', '5.8'),
    Row('institutionmanager',    'institutions', '*', 'retrieve', '*', '4.3.22'),
    Row('professor',             'institutions', '*', 'retrieve', '*', '1.3.15'),
    Row('candidate',             'institutions', '*', 'retrieve', '*', '3.3.10'),
    Row('helpdeskadmin',         'institutions', '*', 'retrieve', '*', '5.8'),
    Row('helpdeskuser',          'institutions', '*', 'retrieve', '*', '5.8'),
    Row('helpdeskadmin',         'institutions', '*', 'create', '*', '5.2.5'),
    Row('helpdeskadmin',         'institutions', '*', 'update', '*', '5.2.5'),
    Row('helpdeskadmin',         'institutions', '*', 'destroy', '*', '5.2.5'),
    Row('institutionmanager',    'institutions', 'organization', 'partial_update', 'owned', ''),
    Row('institutionmanager',    'institutions', 'regulatory_framework', 'partial_update', 'owned', ''),

    Row('institutionmanager',    'departments', '*', 'list', '*', '4.3.21'),
    Row('professor',             'departments', '*', 'list', '*', '1.3.14'),
    Row('candidate',             'departments', '*', 'list', '*', ''),
    Row('helpdeskadmin',         'departments', '*', 'list', '*', '5.2.5'),
    Row('helpdeskuser',          'departments', '*', 'list', '*', '5.2.5'),
    Row('institutionmanager',    'departments', '*', 'retrieve', '*', '4.3.10'),
    Row('professor',             'departments', '*', 'retrieve', '*', '1.2.1'),
    Row('candidate',             'departments', '*', 'retrieve', '*', '3.3.1'),
    Row('helpdeskadmin',         'departments', '*', 'retrieve', '*', '5.2.5'),
    Row('helpdeskuser',          'departments', '*', 'retrieve', '*', '5.2.5'),
    Row('helpdeskadmin',         'departments', '*', 'create', '*', '5.2.5'),
    Row('helpdeskadmin',         'departments', '*', 'update', '*', '5.2.5'),
    Row('helpdeskadmin',         'departments', '*', 'destroy', '*', '5.2.5'),

    Row('institutionmanager',    'subjects-areas', '*', 'list', '*', '4.3.10'),
    Row('professor',             'subjects-areas', '*', 'list', '*', '3.3.1'),
    Row('candidate',             'subjects-areas', '*', 'list', '*', '3.3.1'),
    Row('helpdeskadmin',         'subjects-areas', '*', 'list', '*', ''),
    Row('helpdeskuser',          'subjects-areas', '*', 'list', '*', ''),
    Row('institutionmanager',    'subjects-areas', '*', 'retrieve', '*', '4.3.10'),
    Row('professor',             'subjects-areas', '*', 'retrieve', '*', '1.3.3'),
    Row('candidate',             'subjects-areas', '*', 'retrieve', '*', '3.3.2'),
    Row('helpdeskadmin',         'subjects-areas', '*', 'retrieve', '*', ''),
    Row('helpdeskuser',          'subjects-areas', '*', 'retrieve', '*', ''),
    Row('helpdeskadmin',         'subjects-areas', '*', 'create', '*', ''),
    Row('helpdeskadmin',         'subjects-areas', '*', 'update', '*', ''),
    Row('helpdeskadmin',         'subjects-areas', '*', 'destroy', '*', ''),
    Row('institutionmanager',    'subjects', '*', 'list', '*', '4.3.10'),
    Row('professor',             'subjects', '*', 'list', '*', '3.3.1'),
    Row('candidate',             'subjects', '*', 'list', '*', '3.3.1'),
    Row('helpdeskadmin',         'subjects', '*', 'list', '*', ''),
    Row('helpdeskuser',          'subjects', '*', 'list', '*', ''),
    Row('institutionmanager',    'subjects', '*', 'retrieve', '*', '4.3.10'),
    Row('professor',             'subjects', '*', 'retrieve', '*', '1.3.3'),
    Row('candidate',             'subjects', '*', 'retrieve', '*', '3.3.2'),
    Row('helpdeskadmin',         'subjects', '*', 'retrieve', '*', ''),
    Row('helpdeskuser',          'subjects', '*', 'retrieve', '*', ''),
    Row('helpdeskadmin',         'subjects', '*', 'create', '*', ''),
    Row('helpdeskadmin',         'subjects', '*', 'update', '*', ''),
    Row('helpdeskadmin',         'subjects', '*', 'destroy', '*', ''),

    Row('institutionmanager',    'positions', '*', 'list', 'owned', '4.3.9'),
    Row('professor',             'positions', '*', 'list', '*', '3.3.2'),
    Row('candidate',             'positions', '*', 'list', '*', '3.3.2'),
    Row('helpdeskadmin',         'positions', '*', 'list', '*', '5.13'),
    Row('helpdeskuser',          'positions', '*', 'list', '*', '5.13'),
    Row('institutionmanager',    'positions', '*', 'retrieve', 'owned', '4.3.9'),
    Row('professor',             'positions', '*', 'retrieve', '*', '1.3'),
    Row('candidate',             'positions', '*', 'retrieve', '*', '3.3.4'),
    Row('helpdeskadmin',         'positions', '*', 'retrieve', '*', '5.14'),
    Row('helpdeskuser',          'positions', '*', 'retrieve', '*', '5.14'),
    Row('institutionmanager',    'positions', '*', 'create', '*', '4.3.10'),
    Row('institutionmanager',    'positions', 'state', 'partial_update', 'before_open', '4.3.11.b'),
    Row('institutionmanager',    'positions', 'state', 'partial_update', 'electing', '4.3.11.g'),
    Row('institutionmanager',    'positions', 'state', 'partial_update', 'electing', '4.3.11.h'),
    Row('institutionmanager',    'positions', 'starts_at', 'partial_update', 'before_open', '4.3.11.c'),
    Row('institutionmanager',    'positions', 'ends_at', 'partial_update', 'before_open', '4.3.11.c'),
    Row('institutionmanager',    'positions', 'electors', 'partial_update', 'closed, decision_to_form_electors_file', '4.3.14'),
    Row('institutionmanager',    'positions', 'committee', 'partial_update', 'electing, check_electors_completed, electors_meeting', '4.3.15'),
    Row('institutionmanager',    'positions', 'elected', 'partial_update', 'electing, committee_meeting', '4.3.11.f'),
]

tb.update(PERMISSIONS)
row = Row(role='*', resource='positions', field='*',
          action='retrieve', state='*', section='5.*')
results = tb.match(row, expand={'role'})
result_list = list(results)
result_list.sort()
import pprint
pprint.pprint(result_list)
