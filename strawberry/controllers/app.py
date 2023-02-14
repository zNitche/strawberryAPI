from strawberry.communication.response import Response
from strawberry.communication.file_response import FileResponse
from strawberry.routes.default.errors import errors


class App:
    def __init__(self, static_files_path="/static",
                 debug_mode=False):

        self.debug_mode = debug_mode
        self.static_files_path = static_files_path

        self.blueprints = []
        self.errors_routes = errors.routes

    async def requests_handler(self, client_addr, request):
        response = self.raise_error(500)

        if request:
            self.print_debug(f"request header from {client_addr} :{request.header}")
            self.print_debug(f"request body from {client_addr} :{request.body} | {type(request.body)}")

            if self.__check_if_requested_static_file(request):
                self.print_debug("requested static file")

                target = request.target.split("static/")[-1]
                response = self.__get_static_file(target)

            else:
                self.print_debug("requested route")
                response = self.__process_route(request)

            self.print_debug(f"response string for {client_addr}: '{response.get_response_string()}'")

        return response.get_response_string()

    def __get_route_for_url(self, url):
        target_route = None

        for blueprint in self.blueprints:
            for route in blueprint.routes:
                if route.match_url(url):
                    target_route = route
                    break

        self.print_debug(f"route for url '{url}': {target_route.handler.__name__ if target_route else None}")

        return target_route

    def __get_error_route_by_status_code(self, status_code):
        target_error_route = None

        for route in self.errors_routes:
            if route.status_code == status_code:
                target_error_route = route
                break

        self.print_debug(
            f"err_route for '{status_code}': {target_error_route.handler.__name__ if target_error_route else None}")

        return target_error_route

    def __check_if_requested_static_file(self, request):
        # Check if request url ends with file extension and request method == GET
        url_extension = request.target.split(".")
        is_request_get = True if (request.method == "GET") else False

        return True if (len(url_extension) > 1 and is_request_get) else False

    def __get_static_file(self, target):
        self.print_debug(f"static file target: {target}")

        return FileResponse(f"{self.static_files_path}/{target}")

    def __process_route(self, request):
        route = self.__get_route_for_url(request.target)
        response = self.raise_error(404)

        if route:
            response = route.handler(request) if request.method in route.methods else Response(405)

        return response

    def register_blueprint(self, route):
        self.blueprints.append(route)

    def raise_error(self, status_code):
        route = self.__get_error_route_by_status_code(status_code)
        response = route.handler() if route else Response(404)

        return response

    def url_for(self, endpoint_name):
        endpoint_url = None

        for blueprint in self.blueprints:
            for route in blueprint.routes:
                route_full_name = f"{blueprint.name}.{route.handler.__name__}"

                if route_full_name == endpoint_name:
                    endpoint_url = route.url
                    break

        return endpoint_url

    def print_debug(self, message):
        if self.debug_mode:
            print(f"[APP] - {message}")
