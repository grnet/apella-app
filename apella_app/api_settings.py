multilangfields_resource = {
    'model': 'apella.models.MultiLangFields',
    'field_schema': {
        'fields': ['id', 'el', 'en']
    }
}

position_resource = {
    'model': 'apella.models.Position',
    'field_schema': {
        'fields': ['id', 'url', 'title', 'description', 'discipline', 'author',
                   'department', 'subject_area', 'subject', 'fek',
                   'fek_posted_at', 'assistants', 'electors', 'committee',
                   'state', 'starts_at', 'ends_at', 'created_at',
                   'updated_at'],
        'read_only_fields': ['id', 'url', 'created_at', 'updated_at'],
        'serializers': ['apella.serializers.mixins.PositionValidatorMixin']
    },
    'filter_fields': ['title', ],
    'allowable_operations': ['list', 'retrieve', 'create', 'update', 'delete']
}

apellauser_resource = {
    'model': 'apella.models.ApellaUser',
    'field_schema': {
        'fields': ['id', 'url', 'username', 'password', 'email', 'role',
                   'first_name', 'last_name', 'father_name',
                   'id_passport', 'mobile_phone_number',
                   'home_phone_number'],
        'read_only_fields': ['id', 'url'],
        'nested_objects': {
            'first_name': {
                'source': 'first_name',
                'field_schema': {'fields': ['el', 'en']}
            },
            'last_name': {
                'source': 'last_name',
                'field_schema': {'fields': ['el', 'en']}
            },
            'father_name': {
                'source': 'father_name',
                'field_schema': {'fields': ['el', 'en']}
            }
        },
        'serializers': ['apella.serializers.mixins.NestedWritableObjectsMixin']
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
        'serializers': ['apella.serializers.mixins.ValidatorMixin']
    },
    'filter_fields': ['candidate', 'position', 'state', ]
}

institution_resource = {
    'model': 'apella.models.Institution',
    'mixins': ['apella.views.mixins.DestroyProtectedObject'],
    'field_schema': {
        'fields': ['id', 'url', 'organization', 'category',
                   'regulatory_framework', 'title'],
        'read_only_fields': ['id', 'url'],
        'nested_objects': {
            'title': {
                'source': 'title',
                'field_schema': {'fields': ['el', 'en']}
            }
        },
        'serializers': ['apella.serializers.mixins.NestedWritableObjectsMixin']
    }
}

school_resource = {
    'model': 'apella.models.School',
    'mixins': ['apella.views.mixins.DestroyProtectedObject'],
    'field_schema': {
        'fields': ['id', 'url', 'institution', 'title'],
        'read_only_fields': ['id', 'url'],
        'nested_objects': {
            'title': {
                'source': 'title',
                'field_schema': {'fields': ['el', 'en']}
            }
        },
        'serializers': ['apella.serializers.mixins.NestedWritableObjectsMixin']
    },
    'filter_fields': ['institution', ]
}

department_resource = {
    'model': 'apella.models.Department',
    'mixins': ['apella.views.mixins.DestroyProtectedObject'],
    'field_schema': {
        'fields': ['id', 'url', 'institution', 'school', 'title'],
        'read_only_fields': ['id', 'url'],
        'nested_objects': {
            'title': {
                'source': 'title',
                'field_schema': {'fields': ['el', 'en']}
            }
        },
        'serializers': ['apella.serializers.mixins.NestedWritableObjectsMixin']
    },
    'filter_fields': ['school', ]
}

subject_area_resource = {
    'model': 'apella.models.SubjectArea',
    'field_schema': {
        'fields': ['id', 'url', 'title'],
        'read_only_fields': ['id', 'url'],
        'nested_objects': {
            'title': {
                'source': 'title',
                'field_schema': {'fields': ['el', 'en']}
            }
        },
        'serializers': ['apella.serializers.mixins.NestedWritableObjectsMixin']
    }
}

subject_resource = {
    'model': 'apella.models.Subject',
    'field_schema': {
        'fields': ['id', 'url', 'area', 'title'],
        'read_only_fields': ['id', 'url'],
        'nested_objects': {
            'title': {
                'source': 'title',
                'field_schema': {'fields': ['el', 'en']}
            }
        },
        'serializers': ['apella.serializers.mixins.NestedWritableObjectsMixin']
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
                   'authority_full_name', 'manager_role',
                   'sub_first_name', 'sub_last_name', 'sub_father_name',
                   'sub_email', 'sub_mobile_phone_number',
                   'sub_home_phone_number'],
        'nested_objects': {
            'user': {
                'source': 'user',
                'field_schema': apellauser_resource['field_schema']
            },
            'sub_first_name': {
                'source': 'sub_first_name',
                'field_schema': multilangfields_resource['field_schema']
            },
            'sub_last_name': {
                'source': 'sub_last_name',
                'field_schema': multilangfields_resource['field_schema']
            },
            'sub_father_name': {
                'source': 'sub_father_name',
                'field_schema': multilangfields_resource['field_schema']
            },
        },
        'serializers': [
            'apella.serializers.mixins.NestedWritableObjectsMixin'],
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
        'serializers': [
            'apella.serializers.mixins.NestedWritableObjectsMixin'],
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
        'serializers': [
            'apella.serializers.mixins.NestedWritableObjectsMixin'],
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
        'multilang': multilangfields_resource,
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
