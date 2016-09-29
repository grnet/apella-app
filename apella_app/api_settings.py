position_resource = {
    'model': 'apella.models.Position',
    'field_schema': {
        'fields': ['id', 'url', 'title', 'description', 'discipline', 'author',
                   'department', 'subject_area', 'subject', 'fek',
                   'fek_posted_at', 'assistants', 'electors', 'committee',
                   'state', 'starts_at', 'ends_at', 'created_at',
                   'updated_at'],
        'read_only_fields': ['id', 'url', 'created_at', 'updated_at'],
        'custom_mixins': ['apella.mixins.PositionMixin']
    },
    'filter_fields': ['title', ],
    'allowable_operations': ['list', 'retrieve', 'create', 'update', 'delete']
}

apellauser_resource = {
    'model': 'apella.models.ApellaUser',
    'field_schema': {
        'fields': ['id', 'url', 'username', 'role'],
        'read_only_fields': ['id', 'url', 'username']
    },
    'filter_fields': ['username', ]
}

candidacy_resource = {
    'model': 'apella.models.Candidacy',
    'field_schema': {
        'fields': ['id', 'url', 'candidate', 'position',
                   'submitted_at', 'state', 'others_can_view',
                   'updated_at'],
        'read_only_fields': ['id', 'url', 'submitted_at', 'updated_at']
    },
    'filter_fields': ['candidate', 'position', 'state', ]
}

institution_resource = {
    'model': 'apella.models.Institution',
    'field_schema': {
        'fields': ['id', 'url', 'title', 'organization',
                   'regulatory_framework'],
        'read_only_fields': ['id', 'url']
    },
    'filter_fields': ['title', ],
}

school_resource = {
    'model': 'apella.models.School',
    'field_schema': {
        'fields': ['id', 'url', 'title', 'institution'],
        'read_only_fields': ['id', 'url']
    },
    'filter_fields': ['title', 'institution', ]
}

department_resource = {
    'model': 'apella.models.Department',
    'field_schema': {
        'fields': ['id', 'url', 'title', 'school'],
        'read_only_fields': ['id', 'url']
    },
    'filter_fields': ['title', 'school', ]
}

subject_area_resource = {
    'model': 'apella.models.SubjectArea',
    'field_schema': {
        'fields': ['id', 'url', 'title'],
        'read_only_fields': ['id', 'url']
    },
    'filter_fields': ['title', ]
}

subject_resource = {
    'model': 'apella.models.Subject',
    'field_schema': {
        'fields': ['id', 'url', 'title', 'area'],
        'read_only_fields': ['id', 'url']
    },
    'filter_fields': ['title', 'area', ]
}

registry_resource = {
    'model': 'apella.models.Registry',
    'field_schema': {
        'fields': ['id', 'url', 'department', 'type', 'members'],
        'read_only_fields': ['id', 'url']
    },
    'filter_fields': ['department', 'type', ]
}

API_SCHEMA = {
    'resources': {
        'positions': position_resource,
        'candidacies': candidacy_resource,
        'users': apellauser_resource,
        'institutions': institution_resource,
        'schools': school_resource,
        'departments': department_resource,
        'subject_areas': subject_area_resource,
        'subjects': subject_resource,
        'registries': registry_resource
    }
}
