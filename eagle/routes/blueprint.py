from eagle.routes.route import Route
from eagle.routes.base.routes_handler import RoutesHandler


class Blueprint(RoutesHandler):
    def __init__(self, name, url_prefix=None):
        super().__init__(name)

        self.url_prefix = url_prefix

    def add_route(self, url, route_handler, methods):
        self.routes.append(Route(url, route_handler, methods))

    def route(self, url, methods=None):
        def wrapper(func):
            route_url = f"{self.url_prefix}{url}" if self.url_prefix else url

            self.add_route(route_url, func, methods)

        return wrapper
