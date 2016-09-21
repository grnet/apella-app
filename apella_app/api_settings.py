position_resource = {
     'model': 'apella.models.Position',
     'fields': ('id', 'url', 'title', 'description', 'discipline', 'author',
                'department', 'subject_area', 'subject', 'fek',
                'fek_posted_at', 'assistants', 'electors', 'committee',
                'state', 'starts_at', 'ends_at'),
     'read_only_fields': ('id', 'url'),
     'filter_fields': ('title',),
     'allowable_operations': (
         'list', 'retrieve', 'create', 'update', 'delete')
}

apellauser_resource = {
    'model': 'apella.models.ApellaUser',
    'fields': ('id', 'url', 'username', 'role'),
    'read_only_fields': ('id', 'url', 'username'),
    'filter_fields': ('username',)
}

candidacy_resource = {
    'model': 'apella.models.Candidacy',
    'fields': ('id', 'url', 'candidate', 'position',
               'submitted_at', 'state', 'files'),
    'read_only_fields': ('id', 'url', 'submitted_at'),
    'filter_fields': ('candidate', 'position', 'state',)
}

institution_resource = {
    'model': 'apella.models.Institution',
    'fields': ('id', 'url', 'title'),
    'read_only_fields': ('id', 'url'),
    'filter_fields': ('title',)
}

school_resource = {
    'model': 'apella.models.School',
    'fields': ('id', 'url', 'title', 'institution'),
    'read_only_fields': ('id', 'url'),
    'filter_fields': ('title', 'institution',)
}

department_resource = {
    'model': 'apella.models.Department',
    'fields': ('id', 'url', 'title', 'school'),
    'read_only_fields': ('id', 'url'),
    'filter_fields': ('title', 'school',)
}

subject_area_resource = {
    'model': 'apella.models.SubjectArea',
    'fields': ('id', 'url', 'title'),
    'read_only_fields': ('id', 'url'),
    'filter_fields': ('title',)
}

subject_resource = {
    'model': 'apella.models.Subject',
    'fields': ('id', 'url', 'title', 'area'),
    'read_only_fields': ('id', 'url'),
    'filter_fields': ('title', 'area',)
}

registry_resource = {
    'model': 'apella.models.Registry',
    'fields': ('id', 'url', 'department', 'type', 'members'),
    'read_only_fields': ('id', 'url'),
    'filter_fields': ('department', 'type',)
}

API_SCHEMA = {
    'resources': {
         'users': apellauser_resource,
         'positions': position_resource,
         'candidacies': candidacy_resource,
         'institutions': institution_resource,
         'schools': school_resource,
         'departments': department_resource,
         'subject_areas': subject_area_resource,
         'subjects': subject_resource,
         'registries': registry_resource
    }
}
