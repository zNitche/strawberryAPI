import network
import socket
import sys
import time
from configs.server_config import ServerConfig
from eagle.utils import machine_utils
from eagle.communication.request import Request


class Server:
    def __init__(self, debug_mode=ServerConfig.DEBUG_MODE):
        self.wlan = None

        self.socket = None

        self.debug_mode = debug_mode
        self.is_running = False

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

    def get_socket_address(self):
        return socket.getaddrinfo("0.0.0.0", ServerConfig.SERVER_PORT)[0][-1]

    def bind_socket(self):
        self.print_debug("binding socket...")

        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.get_socket_address())
        self.socket.listen(1)

        self.print_debug("socket bound...")

    def run_as_client(self):
        self.setup_wlan_as_client()
        self.connect_to_network()
        self.bind_socket()

    def run_as_host(self):
        self.setup_wlan_as_host()
        self.bind_socket()

    def mainloop(self):
        self.print_debug("starting mainloop...")
        self.is_running = True

        if self.wlan is not None and self.socket is not None:
            self.print_debug("mainloop running...")

            while self.wlan.isconnected() and self.is_running:
                connection = None

                try:
                    connection, address = self.socket.accept()
                    self.print_debug(f"connection from: {address}")

                    request_string = (connection.recv(ServerConfig.MAX_CONNECTION_PAYLOAD_LENGTH)).decode("utf-8")

                    self.print_debug(f"request string from {address}: {request_string}")

                    request = Request(request_string)
                    request.create()

                    self.print_debug(f"request from {address}: {request.header}")

                except Exception as e:
                    self.print_debug(f"error occurred: {str(e)}")

                    if self.debug_mode:
                        sys.print_exception(e)

                finally:
                    if connection is not None:
                        connection.close()

                time.sleep(ServerConfig.MAINLOOP_DELAY)
