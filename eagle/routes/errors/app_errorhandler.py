from eagle.routes.errors.error_route import ErrorRoute
from eagle.routes.base.routes_handler import RoutesHandler


class AppErrorHandler(RoutesHandler):
    def __init__(self, name):
        super().__init__(name)

    def add_route(self, status_code, route_handler):
        self.routes.append(ErrorRoute(route_handler, status_code))

    def app_error(self, status_code):
        def wrapper(func):
            self.add_route(status_code, func)

        return wrapper
