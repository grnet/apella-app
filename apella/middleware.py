import traceback
import logging


logger = logging.getLogger('apella')


class ExceptionLoggingMiddleware(object):
    def process_exception(self, request, exception):
        m = ''.join(traceback.format_exc())
        logger.exception(m)
        return None
