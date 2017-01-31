from django.conf import settings

from apimas.modeling.adapters.drf import django_rest
from apella.common import load_config
from apimas.modeling.core import documents as doc

permission_classes = []
authentication_classes = ['rest_framework.authentication.TokenAuthentication']

config = load_config()
adapter = django_rest.DjangoRestAdapter()
spec = config.get('spec')
spec['.endpoint']['permissions'] = settings.PERMISSION_RULES

for resource in spec['api'].values():
    doc.doc_set(
        resource,
        ['.drf_collection', 'permission_classes'],
        permission_classes)
    doc.doc_set(
        resource,
        ['.drf_collection', 'authentication_classes'],
        authentication_classes)

adapter.construct(config.get('spec'))
adapter.apply()
api_urls = adapter.urls
