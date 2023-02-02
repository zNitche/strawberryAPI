from eagle.consts import HTTPConsts, ResponseConsts


class Response:
    def __init__(self, status_code, payload=None, content_type=None):
        self.status_code = status_code

        self.payload = payload
        self.content_type = content_type

    def get_header_message_by_status_code(self):
        status_message = ResponseConsts.RESPONSES_STATUSES_MESSAGES.get(self.status_code)

        return status_message if status_message is not None else ResponseConsts.RESPONSES_STATUSES_MESSAGES.get(500)

    def get_header(self):
        status_message = self.get_header_message_by_status_code()
        status_code = self.status_code if status_message is not None else 500

        header_string = ""
        header_rows = [f"HTTP/1.1 {status_code} {status_message}"]

        header_rows.append(f"Content-Type: {self.content_type}") if self.content_type is not None else ""
        header_rows.append(f"Content-Length: {len(self.payload)}") if self.payload is not None else ""

        for row in header_rows:
            if row is not "":
                header_string += f"{row}\r\n"

        return header_string

    def get_body(self):
        return ""

    def get_response_string(self):
        response_string = f"{self.get_header()}\r\n{self.get_body()}"

        return response_string
