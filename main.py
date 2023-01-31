from eagle.controllers.server import Server
from eagle.controllers.app import App
from configs.server_config import ServerConfig


def main():
    server = Server()
    app = App()

    server.run_as_host() if ServerConfig.HOTSPOT_MODE else server.run_as_client()

    server.set_app(app)
    server.run_mainloop()


if __name__ == '__main__':
    main()
