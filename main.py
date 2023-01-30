from eagle.controllers.server import Server
from eagle.controllers.app import App


def main():
    server = Server()

    # server.run_as_host()
    server.run_as_client()

    app = App(server.mainloop)
    app.run()


if __name__ == '__main__':
    main()
