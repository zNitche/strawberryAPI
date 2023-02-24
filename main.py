from strawberry.controllers.server import Server
from strawberry.controllers.app import App


def create_app():
    app = App(debug_mode=True)

    from routes.home.routes import home
    from routes.api.routes import api

    app.register_blueprint(home)
    app.register_blueprint(api)

    return app


def main():
    server = Server(wifi_ssid="", wifi_password="", debug_mode=True)
    server.run()

    server.set_app(create_app())
    server.run_mainloop()


if __name__ == '__main__':
    main()
