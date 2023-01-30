from eagle.controllers.server import Server


def main():
    server = Server(debug_mode=True)
    server.run_as_client()


if __name__ == '__main__':
    main()
