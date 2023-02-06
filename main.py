from eagle.controllers.server import Server
from eagle.controllers.app import App
from config import ServerConfig
from eagle.utils import machine_utils


def init_app():
    app = App()

    from routes.api import api

    app.register_blueprint(api)

    return app


def main():
    server = Server()

    server.run_as_host() if ServerConfig.HOTSPOT_MODE else server.run_as_client()

    if server.wlan is not None:
        machine_utils.get_onboard_led().on()

        server.set_app(init_app())
        server.run_mainloop()


if __name__ == '__main__':
    main()
