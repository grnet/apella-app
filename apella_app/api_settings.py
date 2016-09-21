position_resource = {
     'model': 'apella.models.Position',
     'fields': ('id', 'url', 'title'),
     'read_only_fields': ('id', 'url'),
     'filter_fields': ('title',),
     'allowable_operations': ('list', 'retrieve', 'create', 'update', 'delete')
}

API_SCHEMA = {
    'resources': {
         'positions': position_resource
    }
}
