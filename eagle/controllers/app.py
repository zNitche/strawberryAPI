from eagle.communication.response import Response
from configs.app_config import AppConfig


class App:
    def __init__(self, debug_mode=AppConfig.DEBUG_MODE):
        self.debug_mode = debug_mode

    def run(self):
        pass

    async def requests_handler(self, client_addr, request):
        response = Response(500)

        if request:
            self.print_debug(f"request header from {client_addr} :{request.header}")
            self.print_debug(f"request body from {client_addr} :{request.body}")

            response = Response(200)

            self.print_debug(f"response string for {client_addr}: {response.get_response_string()}")

        return response.get_response_string()

    def print_debug(self, message):
        if self.debug_mode:
            print(f"[APP] - {message}")
