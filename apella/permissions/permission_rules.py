PERMISSION_RULES = [
    ('assistants', 'list', 'helpdeskadmin', '*', '*', '5.1.2'),
    ('assistants', 'retrieve', 'helpdeskadmin', '*', '*', '5.1.2'),
    ('assistants', 'list', 'helpdeskuser', '*', '*', '5.1.2'),
    ('assistants', 'retrieve', 'helpdeskuser', '*', '*', '5.1.2'),
    ('assistants', 'create', 'institutionmanager', '*', '*', '4.3.7'),
    ('assistants', 'list', 'institutionmanager', '*', '*', '4.3.7'),
    ('assistants', 'retrieve', 'institutionmanager', '*', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'user/first_name/el', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'user/first_name/en', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'user/last_name/el', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'user/last_name/en', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'user/father_name/el', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'user/father_name/en', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'user/id_passport', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'user/home_phone_number', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'user/mobile_phone_number', 'owned', '4.3.7'),
    ('candidacies', 'list', 'assistant', '*', '*', '4.3.16'),
    ('candidacies', 'retrieve', 'assistant', '*', 'owned', '4.3.16'),
    ('candidacies', 'create', 'candidate', '*', '*', '3.3.3'),
    ('candidacies', 'partial_update', 'candidate', 'state', 'owned_open', '3.3.7'),
    ('candidacies', 'list', 'candidate', '*', '*', '3.3.5'),
    ('candidacies', 'retrieve', 'candidate', '*', 'others_can_view', '3.3.5'),
    ('candidacies', 'retrieve', 'candidate', '*', 'owned', '3.3.5'),
    ('candidacies', 'list', 'helpdeskadmin', '*', '*', '5.16'),
    ('candidacies', 'retrieve', 'helpdeskadmin', '*', '*', '5.17'),
    ('candidacies', 'partial_update', 'helpdeskadmin', 'state', 'after_closed_electors_meeting_open', '5.2.3.a'),
    ('candidacies', 'list', 'helpdeskuser', '*', '*', '5.16'),
    ('candidacies', 'retrieve', 'helpdeskuser', '*', '*', '5.17'),
    ('candidacies', 'list', 'institutionmanager', '*', '*', '4.3.16'),
    ('candidacies', 'retrieve', 'institutionmanager', '*', 'owned', '4.3.16'),
    ('candidacies', 'create', 'professor', '*', '*', '1.3.9'),
    ('candidacies', 'partial_update', 'professor', '*', 'owned_open', '1.3.13'),
    ('candidacies', 'list', 'professor', '*', '*', '1.3.3'),
    ('candidacies', 'retrieve', 'professor', '*', 'others_can_view', '1.3.5'),
    ('candidacies', 'retrieve', 'professor', '*', 'owned', '1.3.5'),
    ('candidacies', 'retrieve', 'professor', '*', 'participates', '1.3.5'),
    ('candidates', 'create', 'helpdeskadmin', '*', '*', ''),
    ('candidates', 'list', 'helpdeskadmin', '*', '*', '5.1.2'),
    ('candidates', 'partial_update', 'helpdeskadmin', '*', '*', '5.1.3'),
    ('candidates', 'retrieve', 'helpdeskadmin', '*', '*', '5.1.3'),
    ('candidates', 'list', 'helpdeskuser', '*', '*', '5.1.2'),
    ('candidates', 'retrieve', 'helpdeskuser', '*', '*', '5.1.3'),
    ('departments', 'list', 'assistant', '*', '*', ''),
    ('departments', 'retrieve', 'assistant', '*', '*', ''),
    ('departments', 'list', 'candidate', '*', '*', ''),
    ('departments', 'retrieve', 'candidate', '*', '*', '3.3.1'),
    ('departments', 'create', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('departments', 'destroy', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('departments', 'list', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('departments', 'partial_update', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('departments', 'retrieve', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('departments', 'update', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('departments', 'list', 'helpdeskuser', '*', '*', '5.2.5'),
    ('departments', 'retrieve', 'helpdeskuser', '*', '*', '5.2.5'),
    ('departments', 'list', 'institutionmanager', '*', '*', '4.3.21'),
    ('departments', 'retrieve', 'institutionmanager', '*', '*', '4.3.10'),
    ('departments', 'list', 'professor', '*', '*', '1.3.14'),
    ('departments', 'retrieve', 'professor', '*', '*', '1.2.1'),
    ('helpdeskusers', 'create', 'helpdeskadmin', '*', '*', ''),
    ('helpdeskusers', 'list', 'helpdeskadmin', '*', '*', ''),
    ('helpdeskusers', 'retrieve', 'helpdeskadmin', '*', '*', ''),
    ('helpdeskusers', 'partial_update', 'helpdeskadmin', 'user.el', '*', ''),
    ('helpdeskusers', 'partial_update', 'helpdeskadmin', 'user.email', '*', ''),
    ('helpdeskusers', 'partial_update', 'helpdeskadmin', 'user.en', '*', ''),
    ('institution-managers', 'list', 'helpdeskadmin', '*', '*', ''),
    ('institution-managers', 'create', 'helpdeskadmin', '*', '*', ''),
    ('institution-managers', 'partial_update', 'helpdeskadmin', '*', '*', ''),
    ('institutions', 'list', 'assistant', '*', '*', ''),
    ('institutions', 'retrieve', 'assistant', '*', '*', ''),
    ('institutions', 'list', 'candidate', '*', '*', '3.3.10'),
    ('institutions', 'retrieve', 'candidate', '*', '*', '3.3.10'),
    ('institutions', 'create', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('institutions', 'destroy', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('institutions', 'list', 'helpdeskadmin', '*', '*', '5.8'),
    ('institutions', 'partial_update', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('institutions', 'retrieve', 'helpdeskadmin', '*', '*', '5.8'),
    ('institutions', 'update', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('institutions', 'list', 'helpdeskuser', '*', '*', '5.8'),
    ('institutions', 'retrieve', 'helpdeskuser', '*', '*', '5.8'),
    ('institutions', 'list', 'institutionmanager', '*', '*', '4.3.22'),
    ('institutions', 'retrieve', 'institutionmanager', '*', '*', '4.3.22'),
    ('institutions', 'partial_update', 'institutionmanager', 'organization', 'owned', ''),
    ('institutions', 'partial_update', 'institutionmanager', 'regulatory_framework', 'owned', ''),
    ('institutions', 'list', 'professor', '*', '*', '1.3.15'),
    ('institutions', 'retrieve', 'professor', '*', '*', '1.3.15'),
    ('positions', 'list', 'assistant', '*', '*', ''),
    ('positions', 'retrieve', 'assistant', '*', 'owned', ''),
    ('positions', 'list', 'candidate', '*', '*', '3.3.2'),
    ('positions', 'retrieve', 'candidate', '*', 'open', '3.3.4'),
    ('positions', 'list', 'helpdeskadmin', '*', '*', '5.13'),
    ('positions', 'retrieve', 'helpdeskadmin', '*', '*', '5.14'),
    ('positions', 'partial_update', 'helpdeskadmin', 'ends_at', '*', '5.2.4'),
    ('positions', 'partial_update', 'helpdeskadmin', 'starts_at', '*', '5.2.4'),
    ('positions', 'list', 'helpdeskuser', '*', '*', '5.13'),
    ('positions', 'retrieve', 'helpdeskuser', '*', '*', '5.14'),
    ('positions', 'create', 'institutionmanager', '*', '*', '4.3.10'),
    ('positions', 'list', 'institutionmanager', '*', '*', '4.3.9'),
    ('positions', 'retrieve', 'institutionmanager', '*', 'owned', '4.3.9'),
    ('positions', 'partial_update', 'institutionmanager', 'committee', 'electing', '4.3.15'),
    ('positions', 'partial_update', 'institutionmanager', 'elected', 'electing', '4.3.11.f'),
    ('positions', 'partial_update', 'institutionmanager', 'electors', 'closed', '4.3.14'),
    ('positions', 'partial_update', 'institutionmanager', 'ends_at', 'before_open', '4.3.11.c'),
    ('positions', 'partial_update', 'institutionmanager', 'starts_at', 'before_open', '4.3.11.c'),
    ('positions', 'partial_update', 'institutionmanager', 'state', 'before_open', '4.3.11.b'),
    ('positions', 'partial_update', 'institutionmanager', 'state', 'electing', '4.3.11.g'),
    ('positions', 'partial_update', 'institutionmanager', 'state', 'electing', '4.3.11.h'),
    ('positions', 'list', 'professor', '*', '*', '3.3.2'),
    ('positions', 'retrieve', 'professor', '*', 'open', '1.3'),
    ('positions', 'retrieve', 'professor', '*', 'participates', '1.3'),
    ('professors', 'create', 'helpdeskadmin', '*', '*', ''),
    ('professors', 'list', 'helpdeskadmin', '*', '*', '5.1.2'),
    ('professors', 'partial_update', 'helpdeskadmin', '*', '*', '5.1.5'),
    ('professors', 'retrieve', 'helpdeskadmin', '*', '*', '5.1.3'),
    ('professors', 'list', 'helpdeskuser', '*', '*', '5.1.2'),
    ('professors', 'retrieve', 'helpdeskuser', '*', '*', '5.1.3'),
    ('professors', 'list', 'institutionmanager', '*', '*', ''),
    ('professors', 'retrieve', 'institutionmanager', '*', '*', ''),
    ('professors', 'list', 'assistant', '*', '*', ''),
    ('professors', 'retrieve', 'assistant', '*', '*', ''),
    ('registries', 'list', 'candidate', '*', '*', '3.3.9'),
    ('registries', 'retrieve', 'candidate', '*', '*', '3.3.9'),
    ('registries', 'list', 'helpdeskadmin', '*', '*', '5.1.9'),
    ('registries', 'retrieve', 'helpdeskadmin', '*', '*', '5.1.9'),
    ('registries', 'list', 'helpdeskuser', '*', '*', '5.1.9'),
    ('registries', 'retrieve', 'helpdeskuser', '*', '*', '5.1.9'),
    ('registries', 'create', 'institutionmanager', '*', '*', '4.3.3'),
    ('registries', 'list', 'institutionmanager', '*', '*', '4.3.1'),
    ('registries', 'retrieve', 'institutionmanager', '*', '*', '4.3.1'),
    ('registries', 'partial_update', 'institutionmanager', 'members', 'owned', '4.3.6'),
    ('registries', 'list', 'professor', '*', '*', '1.3.14'),
    ('registries', 'retrieve', 'professor', '*', '*', '1.3.14'),
    ('schools', 'list', 'assistant', '*', '*', ''),
    ('schools', 'retrieve', 'assistant', '*', '*', ''),
    ('schools', 'list', 'candidate', '*', '*', ''),
    ('schools', 'retrieve', 'candidate', '*', '*', '3.3.1'),
    ('schools', 'create', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('schools', 'destroy', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('schools', 'list', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('schools', 'partial_update', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('schools', 'retrieve', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('schools', 'update', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('schools', 'list', 'helpdeskuser', '*', '*', '5.2.5'),
    ('schools', 'retrieve', 'helpdeskuser', '*', '*', '5.2.5'),
    ('schools', 'list', 'institutionmanager', '*', '*', '4.3.21'),
    ('schools', 'retrieve', 'institutionmanager', '*', '*', '4.3.10'),
    ('schools', 'list', 'professor', '*', '*', '1.3.14'),
    ('schools', 'retrieve', 'professor', '*', '*', '1.2.1'),
    ('subject-areas', 'list', 'assistant', '*', '*', ''),
    ('subject-areas', 'retrieve', 'assistant', '*', '*', ''),
    ('subject-areas', 'list', 'candidate', '*', '*', '3.3.1'),
    ('subject-areas', 'retrieve', 'candidate', '*', '*', '3.3.2'),
    ('subject-areas', 'create', 'helpdeskadmin', '*', '*', ''),
    ('subject-areas', 'destroy', 'helpdeskadmin', '*', '*', ''),
    ('subject-areas', 'list', 'helpdeskadmin', '*', '*', ''),
    ('subject-areas', 'retrieve', 'helpdeskadmin', '*', '*', ''),
    ('subject-areas', 'update', 'helpdeskadmin', '*', '*', ''),
    ('subject-areas', 'list', 'helpdeskuser', '*', '*', ''),
    ('subject-areas', 'retrieve', 'helpdeskuser', '*', '*', ''),
    ('subject-areas', 'list', 'institutionmanager', '*', '*', '4.3.10'),
    ('subject-areas', 'retrieve', 'institutionmanager', '*', '*', '4.3.10'),
    ('subject-areas', 'list', 'professor', '*', '*', '3.3.1'),
    ('subject-areas', 'retrieve', 'professor', '*', '*', '1.3.3'),
    ('subjects', 'list', 'assistant', '*', '*', ''),
    ('subjects', 'retrieve', 'assistant', '*', '*', ''),
    ('subjects', 'list', 'candidate', '*', '*', '3.3.1'),
    ('subjects', 'retrieve', 'candidate', '*', '*', '3.3.2'),
    ('subjects', 'create', 'helpdeskadmin', '*', '*', ''),
    ('subjects', 'destroy', 'helpdeskadmin', '*', '*', ''),
    ('subjects', 'list', 'helpdeskadmin', '*', '*', ''),
    ('subjects', 'retrieve', 'helpdeskadmin', '*', '*', ''),
    ('subjects', 'update', 'helpdeskadmin', '*', '*', ''),
    ('subjects', 'list', 'helpdeskuser', '*', '*', ''),
    ('subjects', 'retrieve', 'helpdeskuser', '*', '*', ''),
    ('subjects', 'list', 'institutionmanager', '*', '*', '4.3.10'),
    ('subjects', 'retrieve', 'institutionmanager', '*', '*', '4.3.10'),
    ('subjects', 'list', 'professor', '*', '*', '3.3.1'),
    ('subjects', 'retrieve', 'professor', '*', '*', '1.3.3'),
    ('user-interests', 'list', 'helpdeskadmin', '*', '*', ''),
    ('user-interests', 'create', 'helpdeskadmin', '*', '*', ''),
    ('user-interests', 'update', 'helpdeskadmin', '*', '*', ''),
    ('user-interests', 'partial_update', 'helpdeskadmin', '*', '*', '')]
