from eagle.controllers.server import Server


def main():
    server = Server()

    # server.run_as_host()
    server.run_as_client()


if __name__ == '__main__':
    main()
