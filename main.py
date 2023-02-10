from strawberry.controllers.server import Server
from strawberry.controllers.app import App
from strawberry.utils import machine_utils


app = App(debug_mode=True)


def init_app():
    from routes.api import api

    app.register_blueprint(api)

    return app


def main():
    server = Server(wifi_ssid="", wifi_password="", debug_mode=True)
    server.run()

    if server.wlan is not None:
        machine_utils.get_onboard_led().on()

        server.set_app(init_app())
        server.run_mainloop()


if __name__ == '__main__':
    main()
