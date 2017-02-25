import traceback
import logging

logger = logging.getLogger(__name__)


class ExceptionLoggingMiddleware(object):
    def process_exception(self, request, exception):
        m = ''.join(traceback.format_exc())
        logger.exception(m)
        return None


class MultiForwardedHeadersFixMiddleware(object):

    meta_names = (
        'HTTP_HOST',
        'HTTP_X_FORWARDED_FOR',
        'HTTP_X_FORWARDED_HOST',
        'HTTP_X_FORWARDED_SERVER',
    )

    def process_request(self, request):
        meta = request.META
        for meta_name in self.meta_names:
            meta_val = meta.get(meta_name)
            if not meta_val:
                continue
            hosts = [x.strip() for x in meta_val.split(',')]
            if len(hosts) > 1:
                meta[meta_name + '_ALL'] = meta[meta_name]
                meta[meta_name] = hosts[0]
        return None


class RequestLoggingMiddleware(object):
    def process_request(self, request):
        m = 'REQUEST %r %r META %r'
        meta = {
            key: val for key, val in request.META.iteritems()
            if isinstance(val, basestring)
        }
        m %= (request.method, request.path, meta)
        logger.info(m)
        return None
