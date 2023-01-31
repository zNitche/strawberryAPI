class App:
    def __init__(self):
        pass

    def run(self):
        pass

    async def requests_handler(self, client_addr, request):
        response = None

        if request:
            print(f"request header from {client_addr} :{request.header}")
            print(f"request body from {client_addr} :{request.body}")

            response = "HTTP/1.1 200 OK\r\n"

        return response
