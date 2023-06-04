from strawberry.communication.response import Response
from strawberry.communication.file_response import FileResponse
from strawberry.routes.default.errors import errors
from strawberry.utils import files_utils
import sys
import gc


class App:
    def __init__(self, static_files_dirs=None, debug_mode=False):

        self.debug_mode = debug_mode
        self.static_files_dirs = static_files_dirs if not None else ["/static"]

        self.blueprints = []
        self.errors_routes = errors.routes

        self.print_debug("App created...")

    async def requests_handler(self, client_addr, request):
        response = self.raise_error(500)

        try:
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

                self.print_debug(f"response header for {client_addr}: '{response.get_header()}'")

        except Exception as e:
            self.print_debug(f"error occurred: {str(e)}", exception=e)

        finally:
            return response

    def __get_route_for_url(self, url, has_query_params):
        target_route = None
        c_url = url if not has_query_params else url.split("?")[0]

        for blueprint in self.blueprints:
            for route in blueprint.routes:
                if route.match_url(c_url):
                    target_route = route
                    break

        self.print_debug(f"route for url '{url}': {target_route.handler.__name__ if target_route else None}")

        path_parameters = target_route.get_path_parameters_for_url(url) if target_route else None
        self.print_debug(f"path parameters for '{url}': {path_parameters}")

        return target_route, path_parameters

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

        response = self.raise_error(404)

        for static_dir in self.static_files_dirs:
            file_path = f"{static_dir}/{target}"

            if files_utils.check_if_file_exists(file_path):
                response = FileResponse(file_path, is_payload_streamed=True)
                break

        return response

    def __process_route(self, request):
        has_query_params = True if len(request.query_params) > 0 else False

        route, path_parameters = self.__get_route_for_url(request.target, has_query_params=has_query_params)
        response = self.raise_error(404)

        if route:
            request.path_parameters = path_parameters
            response = route.handler(request) if request.method in route.methods else Response(405)

        return response

    def register_blueprint(self, blueprint):
        blueprint.set_app(self)
        self.blueprints.append(blueprint)

    def raise_error(self, status_code):
        route = self.__get_error_route_by_status_code(status_code)
        response = route.handler() if route else Response(404)

        return response

    def url_for(self, endpoint_name, path_parameters=None):
        endpoint_url = None

        for blueprint in self.blueprints:
            for route in blueprint.routes:
                route_full_name = f"{blueprint.name}.{route.handler.__name__}"

                if route_full_name == endpoint_name:
                    endpoint_url = route.url if not route.accepts_path_parameters()\
                        else route.concat_url_with_parameters(path_parameters)

                    break

        return endpoint_url

    def print_debug(self, message, exception=None):
        if self.debug_mode:
            print(f"[APP][FREE_MEM: {int(gc.mem_free() / 1024)}kB] - {message}")

            if exception and isinstance(exception, Exception):
                sys.print_exception(exception)
