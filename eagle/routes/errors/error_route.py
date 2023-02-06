from eagle.routes.base.route_base import RouteBase


class ErrorRoute(RouteBase):
    def __init__(self, handler, status_code):
        super().__init__(handler)
        
        self.status_code = status_code
