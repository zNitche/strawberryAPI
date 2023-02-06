from eagle.communication.response import Response
from eagle.routes.default.errors import errors
from config import AppConfig


class App:
    def __init__(self, debug_mode=AppConfig.DEBUG_MODE):
        self.debug_mode = debug_mode

        self.blueprints = []
        self.errors_routes = errors.routes

    async def requests_handler(self, client_addr, request):
        response = self.handle_app_error(500)

        if request:
            self.print_debug(f"request header from {client_addr} :{request.header}")
            self.print_debug(f"request body from {client_addr} :{request.body} | {type(request.body)}")

            response = self.process_route(request)

            self.print_debug(f"response string for {client_addr}: {response.get_response_string()}")

        return response.get_response_string()

    def get_route_by_url(self, url):
        target_route = None

        for blueprint in self.blueprints:
            for route in blueprint.routes:
                if route.url == url:
                    target_route = route
                    break

        self.print_debug(f"route for url '{url}': {target_route.handler.__name__ if target_route else None}")

        return target_route

    def get_error_route_by_status_code(self, status_code):
        target_error_route = None

        for route in self.errors_routes:
            if route.status_code == status_code:
                target_error_route = route
                break

        self.print_debug(f"err_route for '{status_code}': {target_error_route.handler.__name__ if target_error_route else None}")

        return target_error_route

    def process_route(self, request):
        route = self.get_route_by_url(request.target)
        response = self.handle_app_error(404)

        if route:
            response = route.handler(request) if request.method in route.methods else Response(405)

        return response

    def register_blueprint(self, route):
        self.blueprints.append(route)

    def handle_app_error(self, status_code):
        route = self.get_error_route_by_status_code(status_code)
        response = route.handler() if route else Response(404)

        return response

    def print_debug(self, message):
        if self.debug_mode:
            print(f"[APP] - {message}")
