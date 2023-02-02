from eagle.communication.response import Response


class App:
    def __init__(self):
        pass

    def run(self):
        pass

    async def requests_handler(self, client_addr, request):
        response = Response(500)

        if request:
            print(f"request header from {client_addr} :{request.header}")
            print(f"request body from {client_addr} :{request.body}")

            response = Response(200)

            print(f"response string for {client_addr}: {response.get_response_string()}")

        return response.get_response_string()
