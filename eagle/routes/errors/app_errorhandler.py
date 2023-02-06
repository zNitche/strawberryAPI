from eagle.routes.errors.error_route import ErrorRoute


class AppErrorHandler:
    def __init__(self, name):
        self.name = name

        self.app_errors_routes = []

    def add_app_error_route(self, status_code, route_handler):
        self.app_errors_routes.append(ErrorRoute(route_handler, status_code))

    def app_error(self, status_code):
        def wrapper(func):
            self.add_app_error_route(status_code, func)

        return wrapper
