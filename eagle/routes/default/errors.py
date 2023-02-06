from eagle.routes.errors.app_errorhandler import AppErrorHandler
from eagle.communication.response import Response


errors = AppErrorHandler("errors")


@errors.app_error(404)
def not_found():
    return Response(404)


@errors.app_error(500)
def internal_server_error():
    return Response(500)
