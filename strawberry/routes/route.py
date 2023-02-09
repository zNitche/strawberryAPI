from strawberry.routes.base.route_base import RouteBase


class Route(RouteBase):
    def __init__(self, url, handler, methods):
        super().__init__(handler)

        self.url = url
        self.methods = methods if methods else ["GET"]
