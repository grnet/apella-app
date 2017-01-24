PERMISSION_RULES = [
    ('assistants', 'create', 'institutionmanager', '*', '*', '4.3.7'),
    ('assistants', 'list', 'helpdeskadmin', '*', '*', '5.1.2'),
    ('assistants', 'list', 'helpdeskuser', '*', '*', '5.1.2'),
    ('assistants', 'list', 'institutionmanager', '*', '*', '4.3.7'),
    ('assistants', 'list', 'assistant', '*', '*', ''),
    ('assistants', 'list', 'professor', 'user/email', '*', ''),
    ('assistants', 'list', 'professor', 'user/first_name/el', '*', ''),
    ('assistants', 'list', 'professor', 'user/last_name/el', '*', ''),
    ('assistants', 'list', 'professor', 'user/mobile_phone_number', '*', ''),
    ('assistants', 'list', 'candidate', 'user/email', '*', ''),
    ('assistants', 'list', 'candidate', 'user/first_name/el', '*', ''),
    ('assistants', 'list', 'candidate', 'user/last_name/el', '*', ''),
    ('assistants', 'list', 'candidate', 'user/mobile_phone_number', '*', ''),
    ('assistants', 'update', 'institutionmanager', 'user/father_name/el', 'owned', '4.3.7'),
    ('assistants', 'update', 'institutionmanager', 'user/father_name/en', 'owned', '4.3.7'),
    ('assistants', 'update', 'institutionmanager', 'user/first_name/el', 'owned', '4.3.7'),
    ('assistants', 'update', 'institutionmanager', 'user/first_name/en', 'owned', '4.3.7'),
    ('assistants', 'update', 'institutionmanager', 'user/id_passport', 'owned', '4.3.7'),
    ('assistants', 'update', 'institutionmanager', 'user/last_name/el', 'owned', '4.3.7'),
    ('assistants', 'update', 'institutionmanager', 'user/last_name/en', 'owned', '4.3.7'),
    ('assistants', 'update', 'institutionmanager', 'can_create_registries', 'owned', '4.3.7'),
    ('assistants', 'update', 'institutionmanager', 'can_create_positions', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'user/father_name/el', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'user/father_name/en', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'user/first_name/el', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'user/first_name/en', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'user/id_passport', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'user/last_name/el', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'user/last_name/en', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'can_create_registries', 'owned', '4.3.7'),
    ('assistants', 'partial_update', 'institutionmanager', 'can_create_positions', 'owned', '4.3.7'),
    ('assistants', 'retrieve', 'helpdeskadmin', '*', '*', '5.1.2'),
    ('assistants', 'retrieve', 'helpdeskuser', '*', '*', '5.1.2'),
    ('assistants', 'retrieve', 'institutionmanager', '*', 'owned', '4.3.7'),
    ('assistants', 'retrieve', 'assistant', '*', 'owned_by_assistant', ''),
    ('assistants', 'retrieve', 'professor', 'user/email', '*', ''),
    ('assistants', 'retrieve', 'professor', 'user/first_name/el', '*', ''),
    ('assistants', 'retrieve', 'professor', 'user/last_name/el', '*', ''),
    ('assistants', 'retrieve', 'professor', 'user/mobile_phone_number', '*', ''),
    ('assistants', 'retrieve', 'assistant', 'user/email', '*', ''),
    ('assistants', 'retrieve', 'assistant', 'user/first_name/el', '*', ''),
    ('assistants', 'retrieve', 'assistant', 'user/last_name/el', '*', ''),
    ('assistants', 'retrieve', 'assistant', 'user/mobile_phone_number', '*', ''),
    ('assistants', 'update', 'assistant', 'user/email', 'owned_by_assistant', '4.3.7'),
    ('assistants', 'update', 'assistant', 'user/home_phone_number', 'owned_by_assistant', '4.3.7'),
    ('assistants', 'update', 'assistant', 'user/mobile_phone_number', 'owned_by_assistant', '4.3.7'),
    ('assistants', 'partial_update', 'assistant', 'user/home_phone_number', 'owned_by_assistant', '4.3.7'),
    ('assistants', 'partial_update', 'assistant', 'user/mobile_phone_number', 'owned_by_assistant', '4.3.7'),
    ('assistants', 'partial_update', 'assistant', 'user/email', 'owned_by_assistant', '4.3.7'),
    ('assistants', 'verify_user', 'helpdeskadmin', '*', '*', ''),
    ('assistants', 'verify_user', 'helpdeskuser', '*', '*', ''),
    ('assistants', 'verify_user', 'institutionmanager', '*', 'owned', ''),
    ('assistants', 'reject_user', 'helpdeskadmin', '*', '*', ''),
    ('assistants', 'reject_user', 'helpdeskuser', '*', '*', ''),
    ('assistants', 'reject_user', 'institutionmanager', '*', 'owned', ''),
    ('candidacies', 'create', 'candidate', '*', '*', '3.3.3'),
    ('candidacies', 'create', 'professor', '*', '*', '1.3.9'),
    ('candidacies', 'create', 'helpdeskadmin', '*', '*', '1.3.9'),
    ('candidacies', 'list', 'assistant', '*', '*', '4.3.16'),
    ('candidacies', 'list', 'candidate', '*', '*', '3.3.5'),
    ('candidacies', 'list', 'helpdeskadmin', '*', '*', '5.16'),
    ('candidacies', 'list', 'helpdeskuser', '*', '*', '5.16'),
    ('candidacies', 'list', 'institutionmanager', '*', '*', '4.3.16'),
    ('candidacies', 'list', 'professor', '*', '*', '1.3.3'),
    ('candidacies', 'update', 'helpdeskadmin', 'state', 'after_closed_electors_meeting_open', '5.2.3.a'),
    ('candidacies', 'update', 'professor', 'others_can_view', 'owned', ''),
    ('candidacies', 'update', 'professor', 'state', 'owned_open', '1.3.13'),
    ('candidacies', 'update', 'professor', 'self_evaluation_report', 'five_before_electors_meeting', ''),
    ('candidacies', 'update', 'professor', 'attachment_files', 'one_before_electors_meeting', ''),
    ('candidacies', 'update', 'candidate', 'others_can_view', 'owned', ''),
    ('candidacies', 'update', 'candidate', 'state', 'owned_open', '3.3.7'),
    ('candidacies', 'update', 'candidate', 'self_evaluation_report', 'five_before_electors_meeting', ''),
    ('candidacies', 'update', 'candidate', 'attachment_files', 'one_before_electors_meeting', ''),
    ('candidacies', 'partial_update', 'candidate', 'state', 'owned_open', '3.3.7'),
    ('candidacies', 'partial_update', 'helpdeskadmin', 'state', 'after_closed_electors_meeting_open', '5.2.3.a'),
    ('candidacies', 'partial_update', 'professor', 'state', 'owned_open', '1.3.13'),
    ('candidacies', 'partial_update', 'professor', 'self_evaluation_report', 'five_before_electors_meeting', ''),
    ('candidacies', 'partial_update', 'professor', 'attachment_files', 'one_before_electors_meeting', ''),
    ('candidacies', 'partial_update', 'candidate', 'self_evaluation_report', 'five_before_electors_meeting', ''),
    ('candidacies', 'partial_update', 'candidate', 'attachment_files', 'one_before_electors_meeting', ''),
    ('candidacies', 'retrieve', 'assistant', '*', 'owned', '4.3.16'),
    ('candidacies', 'retrieve', 'candidate', '*', 'others_can_view', '3.3.5'),
    ('candidacies', 'retrieve', 'candidate', '*', 'owned', '3.3.5'),
    ('candidacies', 'retrieve', 'helpdeskadmin', '*', '*', '5.17'),
    ('candidacies', 'retrieve', 'helpdeskuser', '*', '*', '5.17'),
    ('candidacies', 'retrieve', 'institutionmanager', '*', 'owned', '4.3.16'),
    ('candidacies', 'retrieve', 'professor', '*', 'others_can_view', '1.3.5'),
    ('candidacies', 'retrieve', 'professor', '*', 'owned', '1.3.5'),
    ('candidacies', 'retrieve', 'professor', '*', 'participates', '1.3.5'),
    ('candidacies', 'history', 'institutionmanager', '*', 'owned', '4.3.9'),
    ('candidacies', 'history', 'assistant', '*', 'owned', '4.3.9'),
    ('candidacies', 'history', 'professor', '*', 'participates', '4.3.9'),
    ('candidacies', 'history', 'candidate', '*', 'owned', '4.3.9'),
    ('candidacies', 'upload', 'candidate', '*', 'owned', ''),
    ('candidacies', 'upload', 'professor', '*', 'owned', ''),
    ('candidates', 'list', 'helpdeskadmin', '*', '*', '5.1.2'),
    ('candidates', 'list', 'helpdeskuser', '*', '*', '5.1.2'),
    ('candidates', 'update', 'helpdeskadmin', '*', '*', '5.1.3'),
    ('candidates', 'partial_update', 'helpdeskadmin', '*', '*', '5.1.3'),
    ('candidates', 'retrieve', 'helpdeskadmin', '*', '*', '5.1.3'),
    ('candidates', 'retrieve', 'helpdeskuser', '*', '*', '5.1.3'),
    ('candidates', 'retrieve', 'candidate', '*', 'owned', '3'),
    ('candidates', 'upload', 'candidate', '*', 'owned', '3'),
    ('candidates', 'sync_candidacies', 'candidate', '*', 'owned', ''),
    ('candidates', 'request_verification', 'candidate', '*', 'owned', ''),
    ('candidates', 'request_changes', 'helpdeskadmin', '*', '*', ''),
    ('candidates', 'request_changes', 'helpdeskuser', '*', '*', ''),
    ('candidates', 'verify_user', 'helpdeskadmin', '*', '*', ''),
    ('candidates', 'verify_user', 'helpdeskuser', '*', '*', ''),
    ('candidates', 'reject_user', 'helpdeskadmin', '*', '*', ''),
    ('candidates', 'reject_user', 'helpdeskuser', '*', '*', ''),
    ('departments', 'create', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('departments', 'destroy', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('departments', 'list', 'anonymous', '*', '*', ''),
    ('departments', 'list', 'assistant', '*', '*', ''),
    ('departments', 'list', 'candidate', '*', '*', ''),
    ('departments', 'list', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('departments', 'list', 'helpdeskuser', '*', '*', '5.2.5'),
    ('departments', 'list', 'institutionmanager', '*', '*', '4.3.21'),
    ('departments', 'list', 'professor', '*', '*', '1.3.14'),
    ('departments', 'retrieve', 'assistant', '*', '*', ''),
    ('departments', 'retrieve', 'candidate', '*', '*', '3.3.1'),
    ('departments', 'retrieve', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('departments', 'retrieve', 'helpdeskuser', '*', '*', '5.2.5'),
    ('departments', 'retrieve', 'institutionmanager', '*', '*', '4.3.10'),
    ('departments', 'retrieve', 'professor', '*', '*', '1.2.1'),
    ('departments', 'update', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('departments', 'partial_update', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('departments', 'update', 'institutionmanager', 'dep_number', '*', '5.2.5'),
    ('departments', 'partial_update', 'institutionmanager', 'dep_number', '*', '5.2.5'),
    ('helpdeskusers', 'create', 'helpdeskadmin', '*', '*', ''),
    ('helpdeskusers', 'list', 'helpdeskadmin', '*', '*', ''),
    ('helpdeskusers', 'update', 'helpdeskadmin', 'user/email', '*', ''),
    ('helpdeskusers', 'partial_update', 'helpdeskadmin', 'user/email', '*', ''),
    ('helpdeskusers', 'retrieve', 'helpdeskadmin', '*', '*', ''),
    ('institution-managers', 'list', 'helpdeskadmin', '*', '*', ''),
    ('institution-managers', 'list', 'professor', 'id', '*', ''),
    ('institution-managers', 'list', 'professor', 'user/id', '*', ''),
    ('institution-managers', 'list', 'professor', 'user/role', '*', ''),
    ('institution-managers', 'list', 'professor', 'user/email', '*', ''),
    ('institution-managers', 'list', 'professor', 'user/first_name/el', '*', ''),
    ('institution-managers', 'list', 'professor', 'user/last_name/el', '*', ''),
    ('institution-managers', 'list', 'professor', 'user/mobile_phone_number', '*', ''),
    ('institution-managers', 'list', 'professor', 'sub_first_name/el', '*', ''),
    ('institution-managers', 'list', 'professor', 'sub_first_name/en', '*', ''),
    ('institution-managers', 'list', 'professor', 'sub_last_name/el', '*', ''),
    ('institution-managers', 'list', 'professor', 'sub_last_name/en', '*', ''),
    ('institution-managers', 'list', 'professor', 'sub_email', '*', ''),
    ('institution-managers', 'list', 'professor', 'sub_mobile_phone_number', '*', ''),
    ('institution-managers', 'list', 'candidate', 'id', '*', ''),
    ('institution-managers', 'list', 'candidate', 'user/id', '*', ''),
    ('institution-managers', 'list', 'candidate', 'user/role', '*', ''),
    ('institution-managers', 'list', 'candidate', 'user/email', '*', ''),
    ('institution-managers', 'list', 'candidate', 'user/first_name/el', '*', ''),
    ('institution-managers', 'list', 'candidate', 'user/last_name/el', '*', ''),
    ('institution-managers', 'list', 'candidate', 'user/mobile_phone_number', '*', ''),
    ('institution-managers', 'list', 'candidate', 'sub_first_name/el', '*', ''),
    ('institution-managers', 'list', 'candidate', 'sub_first_name/en', '*', ''),
    ('institution-managers', 'list', 'candidate', 'sub_last_name/el', '*', ''),
    ('institution-managers', 'list', 'candidate', 'sub_last_name/en', '*', ''),
    ('institution-managers', 'list', 'candidate', 'sub_email', '*', ''),
    ('institution-managers', 'list', 'candidate', 'sub_mobile_phone_number', '*', ''),
    ('institution-managers', 'list', 'institutionmanager', 'id', '*', ''),
    ('institution-managers', 'list', 'institutionmanager', 'user/id', '*', ''),
    ('institution-managers', 'list', 'institutionmanager', 'user/role', '*', ''),
    ('institution-managers', 'list', 'institutionmanager', 'user/email', '*', ''),
    ('institution-managers', 'list', 'institutionmanager', 'user/first_name/el', '*', ''),
    ('institution-managers', 'list', 'institutionmanager', 'user/last_name/el', '*', ''),
    ('institution-managers', 'list', 'institutionmanager', 'user/mobile_phone_number', '*', ''),
    ('institution-managers', 'list', 'institutionmanager', 'sub_first_name/el', '*', ''),
    ('institution-managers', 'list', 'institutionmanager', 'sub_first_name/en', '*', ''),
    ('institution-managers', 'list', 'institutionmanager', 'sub_last_name/el', '*', ''),
    ('institution-managers', 'list', 'institutionmanager', 'sub_last_name/en', '*', ''),
    ('institution-managers', 'list', 'institutionmanager', 'sub_email', '*', ''),
    ('institution-managers', 'list', 'institutionmanager', 'sub_mobile_phone_number', '*', ''),
    ('institution-managers', 'list', 'assistant', 'id', '*', ''),
    ('institution-managers', 'list', 'assistant', 'user/id', '*', ''),
    ('institution-managers', 'list', 'assistant', 'user/role', '*', ''),
    ('institution-managers', 'list', 'assistant', 'user/email', '*', ''),
    ('institution-managers', 'list', 'assistant', 'user/first_name/el', '*', ''),
    ('institution-managers', 'list', 'assistant', 'user/last_name/el', '*', ''),
    ('institution-managers', 'list', 'assistant', 'user/mobile_phone_number', '*', ''),
    ('institution-managers', 'list', 'assistant', 'sub_first_name/el', '*', ''),
    ('institution-managers', 'list', 'assistant', 'sub_first_name/en', '*', ''),
    ('institution-managers', 'list', 'assistant', 'sub_last_name/el', '*', ''),
    ('institution-managers', 'list', 'assistant', 'sub_last_name/en', '*', ''),
    ('institution-managers', 'list', 'assistant', 'sub_email', '*', ''),
    ('institution-managers', 'list', 'assistant', 'sub_mobile_phone_number', '*', ''),
    ('institution-managers', 'update', 'helpdeskadmin', '*', '*', ''),
    ('institution-managers', 'retrieve', 'helpdeskadmin', '*', '*', ''),
    ('institution-managers', 'partial_update', 'helpdeskadmin', '*', '*', ''),
    ('institution-managers', 'retrieve', 'assistant', '*', 'owned_by_assistant', ''),
    ('institution-managers', 'retrieve', 'institutionmanager', '*', 'owned', ''),
    ('institution-managers', 'retrieve', 'professor', 'id', '*', ''),
    ('institution-managers', 'retrieve', 'professor', 'user/id', '*', ''),
    ('institution-managers', 'retrieve', 'professor', 'user/role', '*', ''),
    ('institution-managers', 'retrieve', 'professor', 'user/email', '*', ''),
    ('institution-managers', 'retrieve', 'professor', 'user/first_name/el', '*', ''),
    ('institution-managers', 'retrieve', 'professor', 'user/last_name/el', '*', ''),
    ('institution-managers', 'retrieve', 'professor', 'user/mobile_phone_number', '*', ''),
    ('institution-managers', 'retrieve', 'professor', 'sub_first_name/el', '*', ''),
    ('institution-managers', 'retrieve', 'professor', 'sub_first_name/en', '*', ''),
    ('institution-managers', 'retrieve', 'professor', 'sub_last_name/el', '*', ''),
    ('institution-managers', 'retrieve', 'professor', 'sub_last_name/en', '*', ''),
    ('institution-managers', 'retrieve', 'professor', 'sub_email', '*', ''),
    ('institution-managers', 'retrieve', 'professor', 'sub_mobile_phone_number', '*', ''),
    ('institution-managers', 'retrieve', 'candidate', 'id', '*', ''),
    ('institution-managers', 'retrieve', 'candidate', 'user/id', '*', ''),
    ('institution-managers', 'retrieve', 'candidate', 'user/role', '*', ''),
    ('institution-managers', 'retrieve', 'candidate', 'user/email', '*', ''),
    ('institution-managers', 'retrieve', 'candidate', 'user/first_name/el', '*', ''),
    ('institution-managers', 'retrieve', 'candidate', 'user/last_name/el', '*', ''),
    ('institution-managers', 'retrieve', 'candidate', 'user/mobile_phone_number', '*', ''),
    ('institution-managers', 'retrieve', 'candidate', 'sub_first_name/el', '*', ''),
    ('institution-managers', 'retrieve', 'candidate', 'sub_first_name/en', '*', ''),
    ('institution-managers', 'retrieve', 'candidate', 'sub_last_name/el', '*', ''),
    ('institution-managers', 'retrieve', 'candidate', 'sub_last_name/en', '*', ''),
    ('institution-managers', 'retrieve', 'candidate', 'sub_email', '*', ''),
    ('institution-managers', 'retrieve', 'candidate', 'sub_mobile_phone_number', '*', ''),
    ('institution-managers', 'retrieve', 'institutionmanager', 'id', '*', ''),
    ('institution-managers', 'retrieve', 'institutionmanager', 'user/id', '*', ''),
    ('institution-managers', 'retrieve', 'institutionmanager', 'user/role', '*', ''),
    ('institution-managers', 'retrieve', 'institutionmanager', 'user/email', '*', ''),
    ('institution-managers', 'retrieve', 'institutionmanager', 'user/first_name/el', '*', ''),
    ('institution-managers', 'retrieve', 'institutionmanager', 'user/last_name/el', '*', ''),
    ('institution-managers', 'retrieve', 'institutionmanager', 'user/mobile_phone_number', '*', ''),
    ('institution-managers', 'retrieve', 'institutionmanager', 'sub_first_name/el', '*', ''),
    ('institution-managers', 'retrieve', 'institutionmanager', 'sub_first_name/en', '*', ''),
    ('institution-managers', 'retrieve', 'institutionmanager', 'sub_last_name/el', '*', ''),
    ('institution-managers', 'retrieve', 'institutionmanager', 'sub_last_name/en', '*', ''),
    ('institution-managers', 'retrieve', 'institutionmanager', 'sub_email', '*', ''),
    ('institution-managers', 'retrieve', 'institutionmanager', 'sub_mobile_phone_number', '*', ''),
    ('institution-managers', 'retrieve', 'assistant', 'id', '*', ''),
    ('institution-managers', 'retrieve', 'assistant', 'user/id', '*', ''),
    ('institution-managers', 'retrieve', 'assistant', 'user/role', '*', ''),
    ('institution-managers', 'retrieve', 'assistant', 'user/email', '*', ''),
    ('institution-managers', 'retrieve', 'assistant', 'user/first_name/el', '*', ''),
    ('institution-managers', 'retrieve', 'assistant', 'user/last_name/el', '*', ''),
    ('institution-managers', 'retrieve', 'assistant', 'user/mobile_phone_number', '*', ''),
    ('institution-managers', 'retrieve', 'assistant', 'sub_first_name/el', '*', ''),
    ('institution-managers', 'retrieve', 'assistant', 'sub_first_name/en', '*', ''),
    ('institution-managers', 'retrieve', 'assistant', 'sub_last_name/el', '*', ''),
    ('institution-managers', 'retrieve', 'assistant', 'sub_last_name/en', '*', ''),
    ('institution-managers', 'retrieve', 'assistant', 'sub_email', '*', ''),
    ('institution-managers', 'retrieve', 'assistant', 'sub_mobile_phone_number', '*', ''),
    ('institution-managers', 'request_verification', 'institutionmanager', '*', 'owned', ''),
    ('institution-managers', 'request_changes', 'helpdeskadmin', '*', '*', ''),
    ('institution-managers', 'request_changes', 'helpdeskuser', '*', '*', ''),
    ('institution-managers', 'verify_user', 'helpdeskadmin', '*', '*', ''),
    ('institution-managers', 'verify_user', 'helpdeskuser', '*', '*', ''),
    ('institution-managers', 'reject_user', 'helpdeskadmin', '*', '*', ''),
    ('institution-managers', 'reject_user', 'helpdeskuser', '*', '*', ''),
    ('institutions', 'create', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('institutions', 'destroy', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('institutions', 'list', 'anonymous', '*', '*', ''),
    ('institutions', 'list', 'assistant', '*', '*', ''),
    ('institutions', 'list', 'candidate', '*', '*', '3.3.10'),
    ('institutions', 'list', 'helpdeskadmin', '*', '*', '5.8'),
    ('institutions', 'list', 'helpdeskuser', '*', '*', '5.8'),
    ('institutions', 'list', 'institutionmanager', '*', '*', '4.3.22'),
    ('institutions', 'list', 'professor', '*', '*', '1.3.15'),
    ('institutions', 'update', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('institutions', 'update', 'institutionmanager', 'organization', 'owned', ''),
    ('institutions', 'update', 'institutionmanager', 'regulatory_framework', 'owned', ''),
    ('institutions', 'partial_update', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('institutions', 'partial_update', 'institutionmanager', 'organization', 'owned', ''),
    ('institutions', 'partial_update', 'institutionmanager', 'regulatory_framework', 'owned', ''),
    ('institutions', 'retrieve', 'assistant', '*', '*', ''),
    ('institutions', 'retrieve', 'candidate', '*', '*', '3.3.10'),
    ('institutions', 'retrieve', 'helpdeskadmin', '*', '*', '5.8'),
    ('institutions', 'retrieve', 'helpdeskuser', '*', '*', '5.8'),
    ('institutions', 'retrieve', 'institutionmanager', '*', '*', '4.3.22'),
    ('institutions', 'retrieve', 'professor', '*', '*', '1.3.15'),
    ('positions', 'create', 'institutionmanager', '*', '*', '4.3.10'),
    ('positions', 'create', 'assistant', '*', 'can_create', 'T1721'),
    ('positions', 'list', 'assistant', '*', '*', ''),
    ('positions', 'list', 'candidate', '*', '*', '3.3.2'),
    ('positions', 'list', 'helpdeskadmin', '*', '*', '5.13'),
    ('positions', 'list', 'helpdeskuser', '*', '*', '5.13'),
    ('positions', 'list', 'institutionmanager', '*', '*', '4.3.9'),
    ('positions', 'list', 'professor', '*', '*', '3.3.2'),
    ('positions', 'update', 'helpdeskadmin', 'ends_at', '*', '5.2.4'),
    ('positions', 'update', 'helpdeskadmin', 'starts_at', '*', '5.2.4'),
    ('positions', 'update', 'institutionmanager', 'electors_regular_internal', 'electing', ''),
    ('positions', 'update', 'institutionmanager', 'electors_regular_external', 'electing', ''),
    ('positions', 'update', 'institutionmanager', 'electors_sub_internal', 'electing', ''),
    ('positions', 'update', 'institutionmanager', 'electors_sub_external', 'electing', ''),
    ('positions', 'update', 'institutionmanager', 'committee', 'electing', '4.3.15'),
    ('positions', 'update', 'institutionmanager', 'committee_internal', 'electing', '4.3.15'),
    ('positions', 'update', 'institutionmanager', 'committee_external', 'electing', '4.3.15'),
    ('positions', 'update', 'institutionmanager', 'elected', 'electing', '4.3.11.f'),
    ('positions', 'update', 'institutionmanager', 'second_best', 'electing', ''),
    ('positions', 'update', 'institutionmanager', 'ends_at', 'before_open', '4.3.11.c'),
    ('positions', 'update', 'institutionmanager', 'starts_at', 'before_open', '4.3.11.c'),
    ('positions', 'update', 'institutionmanager', 'state', 'before_open', '4.3.11.b'),
    ('positions', 'update', 'institutionmanager', 'state', 'electing', '4.3.11.g, 4.3.11.h'),
    ('positions', 'update', 'institutionmanager', 'assistants', 'is_latest', ''),
    ('positions', 'update', 'assistant', 'assistants', 'owned_by_assistant', ''),
    ('positions', 'update', 'institutionmanager', 'electors_meeting_to_set_committee_date', 'electing', ''),
    ('positions', 'update', 'institutionmanager', 'electors_meeting_date', 'electing', ''),
    ('positions', 'update', 'institutionmanager', 'nomination_act_fek', 'electing', ''),
    ('positions', 'update', 'assistant', 'electors_regular_internal', 'electing', ''),
    ('positions', 'update', 'assistant', 'electors_regular_external', 'electing', ''),
    ('positions', 'update', 'assistant', 'electors_sub_internal', 'electing', ''),
    ('positions', 'update', 'assistant', 'electors_sub_external', 'electing', ''),
    ('positions', 'update', 'assistant', 'committee', 'electing', '4.3.15'),
    ('positions', 'update', 'assistant', 'committee_internal', 'electing', '4.3.15'),
    ('positions', 'update', 'assistant', 'committee_external', 'electing', '4.3.15'),
    ('positions', 'update', 'assistant', 'elected', 'electing', '4.3.11.f'),
    ('positions', 'update', 'assistant', 'second_best', 'electing', '4.3.11.f'),
    ('positions', 'update', 'assistant', 'ends_at', 'before_open', '4.3.11.c'),
    ('positions', 'update', 'assistant', 'starts_at', 'before_open', '4.3.11.c'),
    ('positions', 'update', 'assistant', 'state', 'before_open', '4.3.11.b'),
    ('positions', 'update', 'assistant', 'state', 'electing', '4.3.11.g, 4.3.11.h'),
    ('positions', 'update', 'assistant', 'electors_meeting_to_set_committee_date', 'electing', ''),
    ('positions', 'update', 'assistant', 'electors_meeting_date', 'electing', ''),
    ('positions', 'update', 'assistant', 'nomination_act_fek', 'electing', ''),
    ('positions', 'update', 'helpdeskadmin', 'state', '*', ''),
    ('positions', 'partial_update', 'helpdeskadmin', 'ends_at', '*', '5.2.4'),
    ('positions', 'partial_update', 'helpdeskadmin', 'starts_at', '*', '5.2.4'),
    ('positions', 'partial_update', 'helpdeskadmin', 'state', '*', '5.2.4'),
    ('positions', 'partial_update', 'institutionmanager', 'committee', 'electing', '4.3.15'),
    ('positions', 'partial_update', 'institutionmanager', 'elected', 'electing', '4.3.11.f'),
    ('positions', 'partial_update', 'institutionmanager', 'second_best', 'electing', ''),
    ('positions', 'partial_update', 'institutionmanager', 'ends_at', 'before_open', '4.3.11.c'),
    ('positions', 'partial_update', 'institutionmanager', 'starts_at', 'before_open', '4.3.11.c'),
    ('positions', 'partial_update', 'institutionmanager', 'state', 'before_open', '4.3.11.b'),
    ('positions', 'partial_update', 'institutionmanager', 'state', 'electing', '4.3.11.g, 4.3.11.h'),
    ('positions', 'partial_update', 'institutionmanager', 'assistants', 'is_latest', ''),
    ('positions', 'partial_update', 'institutionmanager', 'electors_meeting_to_set_committee_date', 'electing', ''),
    ('positions', 'partial_update', 'institutionmanager', 'electors_meeting_date', 'electing', ''),
    ('positions', 'partial_update', 'institutionmanager', 'nomination_act_fek', 'electing', ''),
    ('positions', 'partial_update', 'assistant', 'assistants', 'owned_by_assistant', ''),
    ('positions', 'partial_update', 'assistant', 'committee', 'electing', '4.3.15'),
    ('positions', 'partial_update', 'assistant', 'elected', 'electing', '4.3.11.f'),
    ('positions', 'partial_update', 'assistant', 'second_best', 'electing', ''),
    ('positions', 'partial_update', 'assistant', 'ends_at', 'before_open', '4.3.11.c'),
    ('positions', 'partial_update', 'assistant', 'starts_at', 'before_open', '4.3.11.c'),
    ('positions', 'partial_update', 'assistant', 'state', 'before_open', '4.3.11.b'),
    ('positions', 'partial_update', 'assistant', 'state', 'electing', '4.3.11.g, 4.3.11.h'),
    ('positions', 'partial_update', 'assistant', 'electors_meeting_to_set_committee_date', 'electing', ''),
    ('positions', 'partial_update', 'assistant', 'electors_meeting_date', 'electing', ''),
    ('positions', 'partial_update', 'assistant', 'nomination_act_fek', 'electing', ''),
    ('positions', 'retrieve', 'assistant', '*', '*', ''),
    ('positions', 'retrieve', 'candidate', '*', '*', '3.3.4'),
    ('positions', 'retrieve', 'helpdeskadmin', '*', '*', '5.14'),
    ('positions', 'retrieve', 'helpdeskuser', '*', '*', '5.14'),
    ('positions', 'retrieve', 'institutionmanager', '*', 'owned', '4.3.9'),
    ('positions', 'retrieve', 'professor', '*', 'open', '1.3'),
    ('positions', 'retrieve', 'professor', '*', '*', '1.3'),
    ('positions', 'history', 'institutionmanager', '*', 'owned', '4.3.9'),
    ('positions', 'history', 'assistant', '*', 'owned', '4.3.9'),
    ('positions', 'history', 'professor', '*', 'participates', '4.3.9'),
    ('positions', 'history', 'helpdeskadmin', '*', '*', '4.3.9'),
    ('positions', 'history', 'helpdeskuser', '*', '*', '4.3.9'),
    ('positions', 'upload', 'institutionmanager', '*', 'owned', ''),
    ('positions', 'upload', 'assistant', '*', 'owned', ''),
    ('professors', 'list', 'assistant', '*', '*', ''),
    ('professors', 'list', 'helpdeskadmin', '*', '*', '5.1.2'),
    ('professors', 'list', 'helpdeskuser', '*', '*', '5.1.2'),
    ('professors', 'list', 'institutionmanager', '*', '*', ''),
    ('professors', 'update', 'helpdeskadmin', '*', '*', '5.1.5'),
    ('professors', 'partial_update', 'helpdeskadmin', '*', '*', '5.1.5'),
    ('professors', 'retrieve', 'assistant', '*', '*', ''),
    ('professors', 'retrieve', 'helpdeskadmin', '*', '*', '5.1.3'),
    ('professors', 'retrieve', 'helpdeskuser', '*', '*', '5.1.3'),
    ('professors', 'retrieve', 'institutionmanager', '*', '*', ''),
    ('professors', 'retrieve', 'professor', '*', 'owned', ''),
    ('professors', 'upload', 'professor', '*', 'owned', ''),
    ('professors', 'sync_candidacies', 'professor', '*', 'owned', ''),
    ('professors', 'request_verification', 'professor', '*', 'owned', ''),
    ('professors', 'request_changes', 'helpdeskadmin', '*', '*', ''),
    ('professors', 'request_changes', 'helpdeskuser', '*', '*', ''),
    ('professors', 'verify_user', 'helpdeskadmin', '*', '*', ''),
    ('professors', 'verify_user', 'helpdeskuser', '*', '*', ''),
    ('professors', 'reject_user', 'helpdeskadmin', '*', '*', ''),
    ('professors', 'reject_user', 'helpdeskuser', '*', '*', ''),
    ('registries', 'create', 'institutionmanager', '*', '*', '4.3.3'),
    ('registries', 'create', 'assistant', '*', 'can_create', 'T1721'),
    ('registries', 'list', 'candidate', '*', '*', '3.3.9'),
    ('registries', 'list', 'helpdeskadmin', '*', '*', '5.1.9'),
    ('registries', 'list', 'helpdeskuser', '*', '*', '5.1.9'),
    ('registries', 'list', 'institutionmanager', '*', '*', '4.3.1'),
    ('registries', 'list', 'assistant', '*', '*', 'T1721'),
    ('registries', 'list', 'professor', '*', '*', '1.3.14'),
    ('registries', 'members', 'institutionmanager', '*', '*', '4.3.6'),
    ('registries', 'members', 'assistant', '*', '*', ''),
    ('registries', 'members', 'helpdeskadmin', '*', '*', ''),
    ('registries', 'members', 'helpdeskuser', '*', '*', ''),
    ('registries', 'members', 'professor', '*', '*', ''),
    ('registries', 'members', 'candidate', '*', '*', ''),
    ('registries', 'retrieve', 'candidate', '*', '*', '3.3.9'),
    ('registries', 'retrieve', 'helpdeskadmin', '*', '*', '5.1.9'),
    ('registries', 'retrieve', 'helpdeskuser', '*', '*', '5.1.9'),
    ('registries', 'retrieve', 'institutionmanager', '*', '*', '4.3.1'),
    ('registries', 'retrieve', 'assistant', '*', '*', ''),
    ('registries', 'retrieve', 'professor', '*', '*', '1.3.14'),
    ('registries', 'update', 'institutionmanager', 'members', 'owned', '4.3.6'),
    ('registries', 'update', 'assistant', 'members', 'can_create', ''),
    ('registries', 'partial_update', 'institutionmanager', 'members', 'owned', '4.3.6'),
    ('registries', 'partial_update', 'assistant', 'members', 'can_create', ''),
    ('registries', 'update', 'helpdeskadmin', '*', '*', ''),
    ('registries', 'partial_update', 'helpdeskadmin', '*', '*', ''),
    ('schools', 'create', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('schools', 'destroy', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('schools', 'list', 'assistant', '*', '*', ''),
    ('schools', 'list', 'candidate', '*', '*', ''),
    ('schools', 'list', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('schools', 'list', 'helpdeskuser', '*', '*', '5.2.5'),
    ('schools', 'list', 'institutionmanager', '*', '*', '4.3.21'),
    ('schools', 'list', 'professor', '*', '*', '1.3.14'),
    ('schools', 'update', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('schools', 'partial_update', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('schools', 'retrieve', 'assistant', '*', '*', ''),
    ('schools', 'retrieve', 'candidate', '*', '*', '3.3.1'),
    ('schools', 'retrieve', 'helpdeskadmin', '*', '*', '5.2.5'),
    ('schools', 'retrieve', 'helpdeskuser', '*', '*', '5.2.5'),
    ('schools', 'retrieve', 'institutionmanager', '*', '*', '4.3.10'),
    ('schools', 'retrieve', 'professor', '*', '*', '1.2.1'),
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
    ('user-interests', 'create', 'professor', '*', '*', ''),
    ('user-interests', 'list', 'professor', '*', '*', ''),
    ('user-interests', 'retrieve', 'professor', '*', 'owned', ''),
    ('user-interests', 'update', 'professor', '*', 'owned', ''),
    ('user-interests', 'partial_update', 'professor', '*', 'owned', ''),
    ('user-interests', 'create', 'candidate', '*', '*', ''),
    ('user-interests', 'list', 'candidate', '*', '*', ''),
    ('user-interests', 'retrieve', 'candidate', '*', 'owned', ''),
    ('user-interests', 'update', 'candidate', '*', 'owned', ''),
    ('user-interests', 'partial_update', 'candidate', '*', 'owned', ''),
    ('users', 'retrieve', 'professor', '*', 'owned', ''),
    ('users', 'retrieve', 'professor', '*', 'is_cocandidate', ''),
    ('users', 'retrieve', 'candidate', '*', 'owned', ''),
    ('users', 'retrieve', 'candidate', '*', 'is_cocandidate', ''),
    ('users', 'retrieve', 'assistant', '*', 'owned', ''),
    ('users', 'retrieve', 'institutionmanager', '*', 'owned', ''),
    ('users', 'retrieve', 'assistant', '*', 'is_candidate', ''),
    ('users', 'retrieve', 'institutionmanager', '*', 'is_candidate', ''),
    ('users', 'retrieve', 'helpdeskadmin', '*', '*', ''),
    ('users', 'retrieve', 'helpdeskuser', '*', '*', ''),
    ('users', 'list', 'helpdeskadmin', '*', '*', ''),
    ('users', 'list', 'helpdeskuser', '*', '*', ''),
    ('users', 'update', 'helpdeskuser', 'is_active', '*', ''),
    ('users', 'update', 'helpdeskadmin', 'is_active', '*', ''),
    ('users', 'partial_update', 'helpdeskadmin', 'is_active', '*', ''),
    ('users', 'partial_update', 'helpdeskuser', 'is_active', '*', ''),
    ('apella-files', 'list', 'helpdeskadmin', '*', '*', ''),
    ('apella-files', 'list', 'helpdeskuser', '*', '*', ''),
    ('apella-files', 'list', 'candidate', '*', '*', ''),
    ('apella-files', 'list', 'professor', '*', '*', ''),
    ('apella-files', 'list', 'institutionmanager', '*', '*', ''),
    ('apella-files', 'list', 'assistant', '*', '*', ''),
    ('apella-files', 'retrieve', 'helpdeskadmin', '*', '*', ''),
    ('apella-files', 'retrieve', 'candidate', '*', 'owned', ''),
    ('apella-files', 'retrieve', 'candidate', '*', 'others_can_view', ''),
    ('apella-files', 'retrieve', 'professor', '*', 'owned', ''),
    ('apella-files', 'retrieve', 'professor', '*', 'others_can_view', ''),
    ('apella-files', 'retrieve', 'institutionmanager', '*', 'owned_by_manager', ''),
    ('apella-files', 'retrieve', 'assistant', '*', 'owned_by_manager', ''),
    ('apella-files', 'destroy', 'professor', '*', 'owned_free', ''),
    ('apella-files', 'destroy', 'candidate', '*', 'owned_free', ''),
    ('apella-files', 'destroy', 'institutionmanager', '*', 'owned_free', ''),
]
