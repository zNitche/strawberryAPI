import network
import sys
import time
import uasyncio
import gc
from strawberry.utils import machine_utils
from strawberry.communication.request import Request
from strawberry.consts import HTTPConsts, ServerConsts


class Server:
    def __init__(self, debug_mode=False,
                 host="0.0.0.0",
                 port=80,
                 wifi_ssid="",
                 wifi_password="",
                 wifi_connections_retries=5,
                 wifi_connection_retries_till_connected=False,
                 wifi_connection_delay=5,
                 hotspot_name="pico_hotspot",
                 hotspot_password="pico_hotspot1234",
                 hotspot_mode=False):

        self.host = host
        self.port = port

        self.wifi_ssid = wifi_ssid
        self.wifi_password = wifi_password

        self.wifi_connections_retries = wifi_connections_retries
        self.wifi_connection_retries_till_connected = wifi_connection_retries_till_connected
        self.wifi_connection_delay = wifi_connection_delay

        self.hotspot_name = hotspot_name
        self.hotspot_password = hotspot_password
        self.hotspot_mode = hotspot_mode

        self.wlan = None
        self.app = None

        self.onboard_led = machine_utils.get_onboard_led()

        self.debug_mode = debug_mode
        self.mainloop = uasyncio.get_event_loop()

        self.led_timer = machine_utils.create_timer()
        self.wifi_reconnect_timer = machine_utils.create_timer() if not self.hotspot_mode else None

    def set_app(self, app):
        self.app = app

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
        machine_utils.init_periodic_timer(self.led_timer,
                                          ServerConsts.LED_BLINK_WIFI_CONNECTED,
                                          self.onboard_led.toggle)

    def __connect_to_network(self):
        tries = 0

        self.wlan.disconnect()

        while ((tries < self.wifi_connections_retries) or self.wifi_connection_retries_till_connected)\
                and (not self.wlan.isconnected()):

            self.print_debug(f"connecting to network: {tries}...")

            self.wlan.connect(self.wifi_ssid, self.wifi_password)
            machine_utils.init_periodic_timer(self.led_timer,
                                              ServerConsts.LED_BLINK_PERIOD_WIFI_CONNECTING,
                                              self.onboard_led.toggle)

            time.sleep(self.wifi_connection_delay)
            tries += 1

        if self.wlan.isconnected():
            self.print_debug(f"connected to '{self.wifi_ssid}'")
            self.print_debug(f"WLAN config: {self.wlan.ifconfig()}")

            machine_utils.init_periodic_timer(self.led_timer,
                                              ServerConsts.LED_BLINK_WIFI_CONNECTED,
                                              self.onboard_led.toggle)

    def __reconnect_to_network(self):
        if not self.wlan.isconnected() and not self.hotspot_mode:
            self.print_debug(f"reconnecting to '{self.wifi_ssid}'")

            self.__connect_to_network()

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

            response = await self.app.requests_handler(client_address, request)

            self.print_debug(f"response header from: {client_address}: {response.get_header()}")
            self.print_debug(f"response is_payload_streamed: {response.is_payload_streamed}")

            if response.is_payload_streamed:
                client_w.write(f"{response.get_header()}\r\n\r\n")
                await client_w.drain()

                for chunk in response.get_body():
                    client_w.write(chunk)
                    await client_w.drain()
            else:
                client_w.write(response.get_response_string())
                await client_w.drain()

        except Exception as e:
            self.print_debug(f"error occurred: {str(e)}", exception=e)

        finally:
            client_w.close()

            await client_w.wait_closed()

            self.print_debug(f"request took: {time.ticks_ms() - start_time}ms")

    def run_mainloop(self):
        self.print_debug("starting mainloop...")

        if self.wlan is not None:
            self.mainloop.create_task(uasyncio.start_server(self.__requests_handler, self.host, self.port))

            if self.wifi_reconnect_timer:
                machine_utils.init_periodic_timer(self.wifi_reconnect_timer,
                                                  ServerConsts.WIFI_RECONNECT_PERIOD,
                                                  self.__reconnect_to_network)

            self.print_debug("mainloop running...")
            self.mainloop.run_forever()

    def stop(self):
        self.mainloop.stop()
        self.mainloop.close()

    def print_debug(self, message, exception=None):
        if self.debug_mode:
            print(f"[SERVER][FREE_MEM: {int(gc.mem_free() / 1024)}kB] - {message}")

            if exception and isinstance(exception, Exception):
                sys.print_exception(exception)
