import network
import sys
import time
import uasyncio
from configs.server_config import ServerConfig
from eagle.utils import machine_utils
from eagle.communication.request import Request
from eagle.consts import RequestsConsts


class Server:
    def __init__(self, debug_mode=ServerConfig.DEBUG_MODE,
                 host=ServerConfig.SERVER_HOST,
                 port=ServerConfig.SERVER_PORT):
        self.host = host
        self.port = port

        self.wlan = None

        self.app = None

        self.debug_mode = debug_mode
        self.mainloop = uasyncio.get_event_loop()

    def set_app(self, app):
        self.app = app

    def print_debug(self, message):
        if self.debug_mode:
            print(f"[SERVER] - {message}")

    def setup_wlan_as_client(self):
        self.print_debug(f"setting up server as client...")

        self.wlan = network.WLAN(network.STA_IF)

        self.wlan.active(True)

    def setup_wlan_as_host(self):
        self.print_debug(f"setting up server as host...")

        self.wlan = network.WLAN(network.AP_IF)
        self.wlan.config(essid=ServerConfig.HOTSPOT_NAME, password=ServerConfig.HOTSPOT_PASSWORD)

        self.wlan.active(True)

        self.print_debug(f"WLAN config: {self.wlan.ifconfig()}")

    def connect_to_network(self):
        tries = 0

        self.wlan.disconnect()

        while (tries < ServerConfig.WIFI_CONNECTION_RETRIES) and (not self.wlan.isconnected()):
            self.print_debug(f"connecting to network: {tries}...")

            self.wlan.connect(ServerConfig.WIFI_SSID, ServerConfig.WIFI_PASSWORD)
            machine_utils.blink_onboard_led()

            time.sleep(ServerConfig.WIFI_CONNECTION_DELAY)
            tries += 1

        if self.wlan.isconnected():
            self.print_debug(f"connected to '{ServerConfig.WIFI_SSID}'")
            self.print_debug(f"WLAN config: {self.wlan.ifconfig()}")

            machine_utils.blink_onboard_led(blinks=3)

    def run_as_client(self):
        self.setup_wlan_as_client()
        self.connect_to_network()

    def run_as_host(self):
        self.setup_wlan_as_host()

    async def load_request(self, request_stream):
        request_header_string = ""

        while True:
            request_line = await request_stream.readline()
            request_line = request_line.decode()

            # header end
            if request_line == "\r\n":
                break

            request_header_string += request_line

        request = Request()
        request.parse_header(request_header_string)

        content_length = int(request.header.get(RequestsConsts.CONTENT_LENGTH))
        request_body_string = await request_stream.readexactly(content_length)

        request.parse_body(request_body_string.decode())

        return request

    async def requests_handler(self, client_r, client_w):
        try:
            client_address = client_w.get_extra_info("peername")

            request = await self.load_request(client_r)
            self.print_debug(f"connection from: {client_address}")

            response = await self.app.requests_handler(client_address, request)

            if response:
                client_w.write(response)

        except Exception as e:
            self.print_debug(f"error occurred: {str(e)}")

            if self.debug_mode:
                sys.print_exception(e)

        finally:
            client_w.close()

            await client_w.wait_closed()

    def run_mainloop(self):
        self.print_debug("starting mainloop...")

        if self.wlan is not None:
            self.mainloop.create_task(uasyncio.start_server(self.requests_handler, self.host, self.port))

            self.print_debug("mainloop running...")
            self.mainloop.run_forever()

    def stop(self):
        self.mainloop.stop()
        self.mainloop.close()
