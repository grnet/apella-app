position_resource = {
    'model': 'apella.models.Position',
    'field_schema': {
        'fields': ['id', 'url', 'title', 'description', 'discipline', 'author',
                   'department', 'subject_area', 'subject', 'fek',
                   'fek_posted_at', 'assistants', 'electors', 'committee',
                   'state', 'starts_at', 'ends_at', 'created_at',
                   'updated_at'],
        'read_only_fields': ['id', 'url', 'created_at', 'updated_at'],
        'serializers': ['apella.mixins.PositionValidatorMixin']
    },
    'filter_fields': ['title', ],
    'allowable_operations': ['list', 'retrieve', 'create', 'update', 'delete']
}

group_resource = {
    'model': 'django.contrib.auth.models.Group',
    'field_schema': {
        'fields': ['id', 'name']
    }
}

apellauser_resource = {
    'model': 'apella.models.ApellaUser',
    'field_schema': {
        'fields': ['id', 'url', 'username', 'password', 'email', 'role',
                   'el', 'en', 'id_passport', 'mobile_phone_number',
                   'home_phone_number', 'groups'],
        'read_only_fields': ['id', 'url'],
        'nested_objects': {
            'el': {
                'source': 'el',
                'field_schema': {'fields': ['first_name', 'last_name',
                                            'father_name']}
            },
            'en': {
                'source': 'en',
                'field_schema': {'fields': ['first_name', 'last_name',
                                            'father_name']}
            }
        },
        'serializers': ['apella.mixins.NestedWritableObjectsMixin']
    },
    'filter_fields': ['username', ]
}

candidacy_resource = {
    'model': 'apella.models.Candidacy',
    'field_schema': {
        'fields': ['id', 'url', 'candidate', 'position',
                   'submitted_at', 'state', 'others_can_view',
                   'updated_at'],
        'read_only_fields': ['id', 'url', 'submitted_at', 'updated_at'],
        'serializers': ['apella.mixins.ValidatorMixin']
    },
    'filter_fields': ['candidate', 'position', 'state', ]
}

institution_resource = {
    'model': 'apella.models.Institution',
    'mixins': ['apella.views.mixins.DestroyProtectedObject'],
    'field_schema': {
        'fields': ['id', 'url', 'organization', 'category',
                   'regulatory_framework', 'el', 'en'],
        'read_only_fields': ['id', 'url'],
        'nested_objects': {
            'el': {
                'source': 'el',
                'field_schema': {'fields': ['title']}
            },
            'en': {
                'source': 'en',
                'field_schema': {'fields': ['title']}
            }
        },
        'serializers': ['apella.mixins.NestedWritableObjectsMixin']
    }
}

school_resource = {
    'model': 'apella.models.School',
    'mixins': ['apella.views.mixins.DestroyProtectedObject'],
    'field_schema': {
        'fields': ['id', 'url', 'institution', 'el', 'en'],
        'read_only_fields': ['id', 'url'],
        'nested_objects': {
            'el': {
                'source': 'el',
                'field_schema': {'fields': ['title']}
            },
            'en': {
                'source': 'en',
                'field_schema': {'fields': ['title']}
            }
        },
        'serializers': ['apella.mixins.NestedWritableObjectsMixin']
    },
    'filter_fields': ['institution', ]
}

department_resource = {
    'model': 'apella.models.Department',
    'mixins': ['apella.views.mixins.DestroyProtectedObject'],
    'field_schema': {
        'fields': ['id', 'url', 'institution', 'school', 'el', 'en'],
        'read_only_fields': ['id', 'url'],
        'nested_objects': {
            'el': {
                'source': 'el',
                'field_schema': {'fields': ['title']}
            },
            'en': {
                'source': 'en',
                'field_schema': {'fields': ['title']}
            }
        },
        'serializers': ['apella.mixins.NestedWritableObjectsMixin']
    },
    'filter_fields': ['school', ]
}

subject_area_resource = {
    'model': 'apella.models.SubjectArea',
    'field_schema': {
        'fields': ['id', 'url', 'el', 'en'],
        'read_only_fields': ['id', 'url'],
        'nested_objects': {
            'el': {
                'source': 'el',
                'field_schema': {'fields': ['title']}
            },
            'en': {
                'source': 'en',
                'field_schema': {'fields': ['title']}
            }
        },
        'serializers': ['apella.mixins.NestedWritableObjectsMixin']
    }
}

subject_resource = {
    'model': 'apella.models.Subject',
    'field_schema': {
        'fields': ['id', 'url', 'area', 'el', 'en'],
        'read_only_fields': ['id', 'url'],
        'nested_objects': {
            'el': {
                'source': 'el',
                'field_schema': {'fields': ['title']}
            },
            'en': {
                'source': 'en',
                'field_schema': {'fields': ['title']}
            }
        },
        'serializers': ['apella.mixins.NestedWritableObjectsMixin']
    },
    'filter_fields': ['area', ]
}

registry_resource = {
    'model': 'apella.models.Registry',
    'field_schema': {
        'fields': ['id', 'url', 'department', 'type', 'members'],
        'read_only_fields': ['id', 'url']
    },
    'filter_fields': ['department', 'type', ]
}

institutionmanager_resource = {
    'model': 'apella.models.InstitutionManager',
    'field_schema': {
        'fields': ['id', 'url', 'user', 'institution', 'authority',
                   'authority_full_name', 'manager_role'],
        'nested_objects': {
            'user': {
                'source': 'user',
                'field_schema': apellauser_resource['field_schema']
            },
        },
        'serializers': ['apella.mixins.NestedWritableUserMixin'],
        'read_only_fields': ['id', 'url']
    },
    'filter_fields': ['institution', 'manager_role', ]
}

professor_resource = {
    'model': 'apella.models.Professor',
    'field_schema': {
        'fields': ['id', 'url', 'user', 'institution', 'department',
                   'rank', 'is_foreign', 'speaks_greek', 'cv_url',
                   'fek', 'discipline_text', 'discipline_in_fek'],
        'nested_objects': {
            'user': {
                'source': 'user',
                'field_schema': apellauser_resource['field_schema']
            },
        },
        'serializers': ['apella.mixins.NestedWritableUserMixin'],
        'read_only_fields': ['id', 'url']
    },
    'filter_fields': ['institution', ]
}

candidate_resource = {
    'model': 'apella.models.Candidate',
    'field_schema': {
        'fields': ['id', 'url', 'user'],
        'nested_objects': {
            'user': {
                'source': 'user',
                'field_schema': apellauser_resource['field_schema']
            },
        },
        'serializers': ['apella.mixins.NestedWritableUserMixin'],
        'read_only_fields': ['id', 'url']
    },
    'filter_fields': []
}

API_SCHEMA = {
    'global': {
        'authentication_classes':
            ['rest_framework.authentication.TokenAuthentication', ],
        'permission_classes': [
            'rest_framework.permissions.IsAuthenticated',
            'apella.permissions.permissions.PermissionRulesCheck', ]
    },
    'resources': {
        'positions': position_resource,
        'candidacies': candidacy_resource,
        'groups': group_resource,
        'users': apellauser_resource,
        'institutions': institution_resource,
        'schools': school_resource,
        'departments': department_resource,
        'subject-areas': subject_area_resource,
        'subjects': subject_resource,
        'registries': registry_resource,
        'institution-managers': institutionmanager_resource,
        'professors': professor_resource,
        'candidates': candidate_resource
    }
}
