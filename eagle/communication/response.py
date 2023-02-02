from eagle.consts import ResponseConsts


class Response:
    def __init__(self, status_code, content_type=None, payload=None):
        self.headers = {}
        self.status_code = status_code
        self.content_type = content_type
        self.payload = payload

    def get_header_message_by_status_code(self):
        status_message = ResponseConsts.RESPONSES_STATUSES_MESSAGES.get(self.status_code)

        return status_message if status_message is not None else ResponseConsts.RESPONSES_STATUSES_MESSAGES.get(500)

    def get_header(self):
        status_message = self.get_header_message_by_status_code()
        status_code = self.status_code if status_message is not None else 500

        header_rows = [f"HTTP/1.1 {status_code} {status_message}"]
        header_rows += [header for header in self.headers]

        header_string = "\r\n".join(header_rows)

        return header_string

    def get_body(self):
        return ""

    def get_response_string(self):
        response_string = f"{self.get_header()}\r\n{self.get_body()}"

        return response_string
