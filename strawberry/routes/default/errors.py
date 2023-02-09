from strawberry.routes.errors.app_errorhandler import AppErrorHandler
from strawberry.communication.response import Response


errors = AppErrorHandler("errors")


@errors.app_error(404)
def not_found():
    return Response(404)


@errors.app_error(500)
def internal_server_error():
    return Response(500)


@errors.app_error(405)
def method_not_allowed():
    return Response(405)


@errors.app_error(400)
def bad_request():
    return Response(400)
