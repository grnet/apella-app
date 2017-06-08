from django.conf import settings

from apimas.drf import django_rest
from apella.common import load_config
from apimas import documents as doc


permission_classes = ['apella.permissions.permissions.TermsPermission', ]
authentication_classes = ['rest_framework.authentication.TokenAuthentication']

config = load_config()
adapter = django_rest.DjangoRestAdapter()
spec = config.get('spec')
spec['api']['.endpoint']['permissions'] = settings.PERMISSION_RULES

for key, resource in spec['api'].iteritems():
    if key.startswith('.'):
        continue
    doc.doc_set(
        resource,
        ['.drf_collection', 'permission_classes'],
        permission_classes)
    doc.doc_set(
        resource,
        ['.drf_collection', 'authentication_classes'],
        authentication_classes)

adapter.construct(config.get('spec'))
api_urls = adapter.urls.values()
