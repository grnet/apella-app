import traceback
import logging

from apella.models import Serials

logger = logging.getLogger('apella')


class ExceptionLoggingMiddleware(object):
    def process_exception(self, request, exception):
        m = ''.join(traceback.format_exc())
        logger.exception(m)
        return None

class RequestSerialMiddleware(object):

    def process_request(self, request):
        request.request_serial = Serials.get_serial('request')
