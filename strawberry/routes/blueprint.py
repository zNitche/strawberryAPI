from strawberry.routes.route import Route
from strawberry.routes.base.routes_handler import RoutesHandler


class Blueprint(RoutesHandler):
    def __init__(self, name, url_prefix=None, templates_dir=""):
        super().__init__(name, templates_dir=templates_dir)

        self.url_prefix = url_prefix

    def add_route(self, url, route_handler, methods):
        self.routes.append(Route(url, route_handler, methods))

    def route(self, url, methods=None):
        def wrapper(func):
            route_url = f"{self.url_prefix}{url}" if self.url_prefix else url

            if not self.check_if_url_added(url):
                self.add_route(route_url, func, methods)

            else:
                raise Exception(f"route for {url} has been already added")

        return wrapper

    def check_if_url_added(self, url):
        found = True if len([route for route in self.routes if route.url == url]) > 0 else False

        return found
