from strawberry.consts import ResponseConsts
from strawberry.consts import HTTPConsts


class Response:
    def __init__(self, status_code=200, content_type=HTTPConsts.CONTENT_TYPE_JSON, payload=None):

        self.headers = {}
        self.status_code = status_code
        self.content_type = content_type

        self.payload = payload
        self.cookies = {}

        self.is_payload_streamed = False

    def get_content_length(self):
        return len(self.payload) if self.payload else 0

    def get_header_message_by_status_code(self):
        status_message = ResponseConsts.RESPONSES_STATUSES_MESSAGES.get(self.status_code)

        return status_message if status_message is not None else ResponseConsts.RESPONSES_STATUSES_MESSAGES.get(500)

    def get_header(self):
        status_message = self.get_header_message_by_status_code()
        status_code = self.status_code if status_message is not None else 500

        header_rows = [f"HTTP/1.1 {status_code} {status_message}",
                       f"CONTENT-TYPE: {self.content_type}",
                       f"CONTENT-LENGTH: {self.get_content_length()}"]

        for header, value in self.headers.items():
            header_rows.append(f"{header}: {value}")

        for cookie_name, cookie_data in self.cookies.items():
            header_rows.append(f"Set-Cookie: {cookie_name}={cookie_data}")

        header_string = "\r\n".join(header_rows)

        return header_string

    def get_body(self):
        return self.payload if self.payload else ""

    def get_response_string(self):
        response_string = f"{self.get_header()}\r\n\r\n{self.get_body()}"

        return response_string
