from eagle.routes.route import Route


class Blueprint:
    def __init__(self, name, url_prefix=None):
        self.name = name
        self.url_prefix = url_prefix

        self.routes = []

    def add_route(self, url, route_handler, methods):
        self.routes.append(Route(url, route_handler, methods))

    def route(self, url, methods=None):
        def wrapper(func):
            self.add_route(url, func, methods)

        return wrapper
