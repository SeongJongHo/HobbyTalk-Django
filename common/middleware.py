from venv import logger
from django.utils.deprecation import MiddlewareMixin

from common.exceptions import BusinessException
from common.response import ResponseGenerator, ResponseMsg

class ExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, e):
        if isinstance(e, BusinessException):
            logger.info(e.message, exc_info=True)
            return ResponseGenerator.build(message=str(e.message), status=e.status)

        logger.error(f"Unhandled Exception: {e}", exc_info=True)
        return ResponseGenerator.build(message=ResponseMsg.FAILED, status=500)