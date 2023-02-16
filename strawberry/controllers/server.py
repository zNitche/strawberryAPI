import network
import sys
import time
import uasyncio
from strawberry.utils import machine_utils
from strawberry.communication.request import Request
from strawberry.consts import HTTPConsts


class Server:
    def __init__(self, debug_mode=False,
                 host="0.0.0.0",
                 port=80,
                 wifi_ssid="",
                 wifi_password="",
                 wifi_connections_retries=5,
                 wifi_connection_delay=5,
                 hotspot_name="pico_hotspot",
                 hotspot_password="pico_hotspot1234",
                 hotspot_mode=False):

        self.host = host
        self.port = port
        self.wifi_ssid = wifi_ssid
        self.wifi_password = wifi_password
        self.wifi_connections_retries = wifi_connections_retries
        self.wifi_connection_delay = wifi_connection_delay
        self.hotspot_name = hotspot_name
        self.hotspot_password = hotspot_password
        self.hotspot_mode = hotspot_mode

        self.wlan = None

        self.app = None

        self.debug_mode = debug_mode
        self.mainloop = uasyncio.get_event_loop()

    def set_app(self, app):
        self.app = app

    def print_debug(self, message):
        if self.debug_mode:
            print(f"[SERVER] - {message}")

    def __setup_wlan_as_client(self):
        self.print_debug(f"setting up server as client...")

        self.wlan = network.WLAN(network.STA_IF)

        self.wlan.active(True)

    def __setup_wlan_as_host(self):
        self.print_debug(f"setting up server as host...")

        self.wlan = network.WLAN(network.AP_IF)
        self.wlan.config(essid=self.hotspot_name, password=self.hotspot_password)

        self.wlan.active(True)

        self.print_debug(f"WLAN config: {self.wlan.ifconfig()}")

    def __connect_to_network(self):
        tries = 0

        self.wlan.disconnect()

        while (tries < self.wifi_connections_retries) and (not self.wlan.isconnected()):
            self.print_debug(f"connecting to network: {tries}...")

            self.wlan.connect(self.wifi_ssid, self.wifi_password)
            machine_utils.blink_onboard_led()

            time.sleep(self.wifi_connection_delay)
            tries += 1

        if self.wlan.isconnected():
            self.print_debug(f"connected to '{self.wifi_ssid}'")
            self.print_debug(f"WLAN config: {self.wlan.ifconfig()}")

            machine_utils.blink_onboard_led(blinks=3)

    def run(self):
        self.__run_as_host() if self.hotspot_mode else self.__run_as_client()

    def __run_as_client(self):
        self.__setup_wlan_as_client()
        self.__connect_to_network()

    def __run_as_host(self):
        self.__setup_wlan_as_host()

    async def __load_request(self, request_stream):
        request_header_string = ""

        while True:
            request_line = await request_stream.readline()
            request_line = request_line.decode()

            # header end
            if request_line == "\r\n":
                break

            request_header_string += request_line

        self.print_debug(f"request header string: {request_header_string}")

        request = Request()
        request.parse_header(request_header_string)

        content_length = request.header.get(HTTPConsts.CONTENT_LENGTH)

        if content_length:
            request_body_string = await request_stream.readexactly(int(content_length))

            request.parse_body(request_body_string.decode())

        self.print_debug(f"request body string: {request.body}")

        return request

    async def __requests_handler(self, client_r, client_w):
        try:
            start_time = time.ticks_ms() if self.debug_mode else None

            client_address = client_w.get_extra_info("peername")

            request = await self.__load_request(client_r)
            self.print_debug(f"connection from: {client_address}")

            response_string = await self.app.requests_handler(client_address, request)

            if response_string:
                client_w.write(response_string)

        except Exception as e:
            self.print_debug(f"error occurred: {str(e)}")

            if self.debug_mode:
                sys.print_exception(e)

        finally:
            client_w.close()

            await client_w.wait_closed()

            if self.debug_mode:
                print(f"request took: {time.ticks_ms() - start_time}ms")

    def run_mainloop(self):
        self.print_debug("starting mainloop...")

        if self.wlan is not None:
            self.mainloop.create_task(uasyncio.start_server(self.__requests_handler, self.host, self.port))

            self.print_debug("mainloop running...")
            self.mainloop.run_forever()

    def stop(self):
        self.mainloop.stop()
        self.mainloop.close()
