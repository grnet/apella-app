PERMISSION_RULES = [
    ('assistants', 'create', 'institutionmanager', '*', '*', '4.3.7'),
    ('assistants', 'list', 'helpdeskadmin', '*', '*', '5.1.2'),
    ('assistants', 'list', 'helpdeskuser', '*', '*', '5.1.2'),
    ('assistants', 'list', 'institutionmanager', '*', '*', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'user/father_name/el', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'user/father_name/en', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'user/first_name/el', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'user/first_name/en', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'user/home_phone_number', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'user/id_passport', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'user/last_name/el', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'user/last_name/en', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'user/mobile_phone_number', 'owned', '4.3.7'),
    ('assistants', 'retrieve', 'helpdeskadmin', '*', '*', '5.1.2'),
    ('assistants', 'retrieve', 'helpdeskuser', '*', '*', '5.1.2'),
    ('assistants', 'retrieve', 'institutionmanager', '*', 'owned', '4.3.7'),
    ('candidacies', 'create', 'candidate', '*', '*', '3.3.3'),
    ('candidacies', 'create', 'professor', '*', '*', '1.3.9'),
    ('candidacies', 'list', 'assistant', '*', '*', '4.3.16'),
    ('candidacies', 'list', 'candidate', '*', '*', '3.3.5'),
    ('candidacies', 'list', 'helpdeskadmin', '*', '*', '5.16'),
    ('candidacies', 'list', 'helpdeskuser', '*', '*', '5.16'),
    ('candidacies', 'list', 'institutionmanager', '*', '*', '4.3.16'),
    ('candidacies', 'list', 'professor', '*', '*', '1.3.3'),
    ('candidacies', 'partial_update', 'candidate', 'state', 'owned_open', '3.3.7'),
    ('candidacies', 'update', 'candidate', 'state', 'owned_open', '3.3.7'),
    ('candidacies', 'partial_update', 'helpdeskadmin', 'state', 'after_closed_electors_meeting_open', '5.2.3.a'),
    ('candidacies', 'partial_update', 'professor', '*', 'owned_open', '1.3.13'),
    ('candidacies', 'retrieve', 'assistant', '*', 'owned', '4.3.16'),
    ('candidacies', 'retrieve', 'candidate', '*', 'others_can_view', '3.3.5'),
    ('candidacies', 'retrieve', 'candidate', '*', 'owned', '3.3.5'),
    ('candidacies', 'retrieve', 'helpdeskadmin', '*', '*', '5.17'),
    ('candidacies', 'retrieve', 'helpdeskuser', '*', '*', '5.17'),
    ('candidacies', 'retrieve', 'institutionmanager', '*', 'owned', '4.3.16'),
    ('candidacies', 'retrieve', 'professor', '*', 'others_can_view', '1.3.5'),
    ('candidacies', 'retrieve', 'professor', '*', 'owned', '1.3.5'),
    ('candidacies', 'retrieve', 'professor', '*', 'participates', '1.3.5'),
    ('candidates', 'create', 'helpdeskadmin', '*', '*', ''),
    ('candidates', 'list', 'helpdeskadmin', '*', '*', '5.1.2'),
    ('candidates', 'list', 'helpdeskuser', '*', '*', '5.1.2'),
    ('candidates', 'partial_update', 'helpdeskadmin', '*', '*', '5.1.3'),
    ('candidates', 'retrieve', 'helpdeskadmin', '*', '*', '5.1.3'),
    ('candidates', 'retrieve', 'helpdeskuser', '*', '*', '5.1.3'),
    ('departments', 'create', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('departments', 'destroy', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('departments', 'list', 'assistant', '*', '*', ''),
    ('departments', 'list', 'candidate', '*', '*', ''),
    ('departments', 'list', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('departments', 'list', 'helpdeskuser', '*', '*', '5.2.5'),
    ('departments', 'list', 'institutionmanager', '*', '*', '4.3.21'),
    ('departments', 'list', 'professor', '*', '*', '1.3.14'),
    ('departments', 'partial_update', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('departments', 'retrieve', 'assistant', '*', '*', ''),
    ('departments', 'retrieve', 'candidate', '*', '*', '3.3.1'),
    ('departments', 'retrieve', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('departments', 'retrieve', 'helpdeskuser', '*', '*', '5.2.5'),
    ('departments', 'retrieve', 'institutionmanager', '*', '*', '4.3.10'),
    ('departments', 'retrieve', 'professor', '*', '*', '1.2.1'),
    ('departments', 'update', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('helpdeskusers', 'create', 'helpdeskadmin', '*', '*', ''),
    ('helpdeskusers', 'list', 'helpdeskadmin', '*', '*', ''),
    ('helpdeskusers', 'partial_update', 'helpdeskadmin', 'user.el', '*', ''),
    ('helpdeskusers', 'partial_update', 'helpdeskadmin', 'user.email', '*', ''),
    ('helpdeskusers', 'partial_update', 'helpdeskadmin', 'user.en', '*', ''),
    ('helpdeskusers', 'retrieve', 'helpdeskadmin', '*', '*', ''),
    ('institution-managers', 'create', 'helpdeskadmin', '*', '*', ''),
    ('institution-managers', 'list', 'helpdeskadmin', '*', '*', ''),
    ('institution-managers', 'partial_update', 'helpdeskadmin', '*', '*', ''),
    ('institutions', 'create', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('institutions', 'destroy', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('institutions', 'list', 'assistant', '*', '*', ''),
    ('institutions', 'list', 'candidate', '*', '*', '3.3.10'),
    ('institutions', 'list', 'helpdeskadmin', '*', '*', '5.8'),
    ('institutions', 'list', 'helpdeskuser', '*', '*', '5.8'),
    ('institutions', 'list', 'institutionmanager', '*', '*', '4.3.22'),
    ('institutions', 'list', 'professor', '*', '*', '1.3.15'),
    ('institutions', 'partial_update', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('institutions', 'partial_update', 'institutionmanager', 'organization', 'owned', ''),
    ('institutions', 'partial_update', 'institutionmanager', 'regulatory_framework', 'owned', ''),
    ('institutions', 'retrieve', 'assistant', '*', '*', ''),
    ('institutions', 'retrieve', 'candidate', '*', '*', '3.3.10'),
    ('institutions', 'retrieve', 'helpdeskadmin', '*', '*', '5.8'),
    ('institutions', 'retrieve', 'helpdeskuser', '*', '*', '5.8'),
    ('institutions', 'retrieve', 'institutionmanager', '*', '*', '4.3.22'),
    ('institutions', 'retrieve', 'professor', '*', '*', '1.3.15'),
    ('institutions', 'update', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('positions', 'create', 'institutionmanager', '*', '*', '4.3.10'),
    ('positions', 'create', 'assistant', '*', 'can_create', 'T1721'),
    ('positions', 'list', 'assistant', '*', '*', ''),
    ('positions', 'list', 'candidate', '*', '*', '3.3.2'),
    ('positions', 'list', 'helpdeskadmin', '*', '*', '5.13'),
    ('positions', 'list', 'helpdeskuser', '*', '*', '5.13'),
    ('positions', 'list', 'institutionmanager', '*', '*', '4.3.9'),
    ('positions', 'list', 'professor', '*', '*', '3.3.2'),
    ('positions', 'partial_update', 'helpdeskadmin', 'ends_at', '*', '5.2.4'),
    ('positions', 'partial_update', 'helpdeskadmin', 'starts_at', '*', '5.2.4'),
    ('positions', 'partial_update', 'institutionmanager', 'committee', 'electing', '4.3.15'),
    ('positions', 'partial_update', 'institutionmanager', 'elected', 'electing', '4.3.11.f'),
    ('positions', 'partial_update', 'institutionmanager', 'electors', 'closed', '4.3.14'),
    ('positions', 'partial_update', 'institutionmanager', 'ends_at', 'before_open', '4.3.11.c'),
    ('positions', 'partial_update', 'institutionmanager', 'starts_at', 'before_open', '4.3.11.c'),
    ('positions', 'partial_update', 'institutionmanager', 'state', 'before_open', '4.3.11.b'),
    ('positions', 'partial_update', 'institutionmanager', 'state', 'electing', '4.3.11.g, 4.3.11.h'),
    ('positions', 'retrieve', 'assistant', '*', 'owned', ''),
    ('positions', 'retrieve', 'candidate', '*', '*', '3.3.4'),
    ('positions', 'retrieve', 'helpdeskadmin', '*', '*', '5.14'),
    ('positions', 'retrieve', 'helpdeskuser', '*', '*', '5.14'),
    ('positions', 'retrieve', 'institutionmanager', '*', 'owned', '4.3.9'),
    ('positions', 'retrieve', 'professor', '*', 'open', '1.3'),
    ('positions', 'retrieve', 'professor', '*', 'participates', '1.3'),
    ('professors', 'create', 'helpdeskadmin', '*', '*', ''),
    ('professors', 'list', 'assistant', '*', '*', ''),
    ('professors', 'list', 'helpdeskadmin', '*', '*', '5.1.2'),
    ('professors', 'list', 'helpdeskuser', '*', '*', '5.1.2'),
    ('professors', 'list', 'institutionmanager', '*', '*', ''),
    ('professors', 'partial_update', 'helpdeskadmin', '*', '*', '5.1.5'),
    ('professors', 'retrieve', 'assistant', '*', '*', ''),
    ('professors', 'retrieve', 'helpdeskadmin', '*', '*', '5.1.3'),
    ('professors', 'retrieve', 'helpdeskuser', '*', '*', '5.1.3'),
    ('professors', 'retrieve', 'institutionmanager', '*', '*', ''),
    ('registries', 'create', 'institutionmanager', '*', '*', '4.3.3'),
    ('registries', 'create', 'assistant', '*', 'can_create', 'T1721'),
    ('registries', 'list', 'candidate', '*', '*', '3.3.9'),
    ('registries', 'list', 'helpdeskadmin', '*', '*', '5.1.9'),
    ('registries', 'list', 'helpdeskuser', '*', '*', '5.1.9'),
    ('registries', 'list', 'institutionmanager', '*', '*', '4.3.1'),
    ('registries', 'list', 'assistant', '*', '*', 'T1721'),
    ('registries', 'list', 'professor', '*', '*', '1.3.14'),
    ('registries', 'partial_update', 'institutionmanager', 'members', 'owned', '4.3.6'),
    ('registries', 'retrieve', 'candidate', '*', '*', '3.3.9'),
    ('registries', 'retrieve', 'helpdeskadmin', '*', '*', '5.1.9'),
    ('registries', 'retrieve', 'helpdeskuser', '*', '*', '5.1.9'),
    ('registries', 'retrieve', 'institutionmanager', '*', '*', '4.3.1'),
    ('registries', 'retrieve', 'professor', '*', '*', '1.3.14'),
    ('schools', 'create', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('schools', 'destroy', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('schools', 'list', 'assistant', '*', '*', ''),
    ('schools', 'list', 'candidate', '*', '*', ''),
    ('schools', 'list', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('schools', 'list', 'helpdeskuser', '*', '*', '5.2.5'),
    ('schools', 'list', 'institutionmanager', '*', '*', '4.3.21'),
    ('schools', 'list', 'professor', '*', '*', '1.3.14'),
    ('schools', 'partial_update', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('schools', 'retrieve', 'assistant', '*', '*', ''),
    ('schools', 'retrieve', 'candidate', '*', '*', '3.3.1'),
    ('schools', 'retrieve', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('schools', 'retrieve', 'helpdeskuser', '*', '*', '5.2.5'),
    ('schools', 'retrieve', 'institutionmanager', '*', '*', '4.3.10'),
    ('schools', 'retrieve', 'professor', '*', '*', '1.2.1'),
    ('schools', 'update', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('subject-areas', 'create', 'helpdeskadmin', '*', '*', ''),
    ('subject-areas', 'destroy', 'helpdeskadmin', '*', '*', ''),
    ('subject-areas', 'list', 'assistant', '*', '*', ''),
    ('subject-areas', 'list', 'candidate', '*', '*', '3.3.1'),
    ('subject-areas', 'list', 'helpdeskadmin', '*', '*', ''),
    ('subject-areas', 'list', 'helpdeskuser', '*', '*', ''),
    ('subject-areas', 'list', 'institutionmanager', '*', '*', '4.3.10'),
    ('subject-areas', 'list', 'professor', '*', '*', '3.3.1'),
    ('subject-areas', 'retrieve', 'assistant', '*', '*', ''),
    ('subject-areas', 'retrieve', 'candidate', '*', '*', '3.3.2'),
    ('subject-areas', 'retrieve', 'helpdeskadmin', '*', '*', ''),
    ('subject-areas', 'retrieve', 'helpdeskuser', '*', '*', ''),
    ('subject-areas', 'retrieve', 'institutionmanager', '*', '*', '4.3.10'),
    ('subject-areas', 'retrieve', 'professor', '*', '*', '1.3.3'),
    ('subject-areas', 'update', 'helpdeskadmin', '*', '*', ''),
    ('subject-areas', 'partial_update', 'helpdeskadmin', '*', '*', ''),
    ('subjects', 'create', 'helpdeskadmin', '*', '*', ''),
    ('subjects', 'destroy', 'helpdeskadmin', '*', '*', ''),
    ('subjects', 'list', 'assistant', '*', '*', ''),
    ('subjects', 'list', 'candidate', '*', '*', '3.3.1'),
    ('subjects', 'list', 'helpdeskadmin', '*', '*', ''),
    ('subjects', 'list', 'helpdeskuser', '*', '*', ''),
    ('subjects', 'list', 'institutionmanager', '*', '*', '4.3.10'),
    ('subjects', 'list', 'professor', '*', '*', '3.3.1'),
    ('subjects', 'retrieve', 'assistant', '*', '*', ''),
    ('subjects', 'retrieve', 'candidate', '*', '*', '3.3.2'),
    ('subjects', 'retrieve', 'helpdeskadmin', '*', '*', ''),
    ('subjects', 'retrieve', 'helpdeskuser', '*', '*', ''),
    ('subjects', 'retrieve', 'institutionmanager', '*', '*', '4.3.10'),
    ('subjects', 'retrieve', 'professor', '*', '*', '1.3.3'),
    ('subjects', 'update', 'helpdeskadmin', '*', '*', ''),
    ('subjects', 'partial_update', 'helpdeskadmin', '*', '*', ''),
    ('user-interests', 'create', 'helpdeskadmin', '*', '*', ''),
    ('user-interests', 'list', 'helpdeskadmin', '*', '*', ''),
    ('user-interests', 'partial_update', 'helpdeskadmin', '*', '*', ''),
    ('user-interests', 'update', 'helpdeskadmin', '*', '*', '')
]
