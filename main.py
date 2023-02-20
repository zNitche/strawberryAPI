from strawberry.controllers.server import Server
from strawberry.controllers.app import App
from strawberry.utils import machine_utils


def create_app():
    app = App(debug_mode=True)

    from routes.home.routes import home
    app.register_blueprint(home)

    return app


def main():
    server = Server(wifi_ssid="", wifi_password="", debug_mode=True)
    server.run()

    if server.wlan is not None:
        machine_utils.get_onboard_led().on()

        app = create_app()

        server.set_app(app)
        server.run_mainloop()


if __name__ == '__main__':
    main()
