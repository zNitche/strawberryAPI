from strawberry.consts import HTTPConsts
from strawberry.parsers.request_payload_parser import RequestPayloadParser


class Request:
    def __init__(self):
        self.protocol = None
        self.target = None
        self.method = None

        self.header = {}
        self.body = ""

        self.path_parameters = {}

        self.payload_parser = RequestPayloadParser()

    def parse_header(self, header_string):
        splitted_request_string = self.split_request_string(header_string)

        if len(splitted_request_string) > 0:
            self.method, self.target, self.protocol = splitted_request_string[0].split()
            splitted_request_string.pop(0)

            self.header = self.parse_request_string(splitted_request_string)

    def parse_body(self, body_string):
        body = body_string.replace("\r", "").replace("\n", "")
        self.body = self.payload_parser.parse_payload(self.header.get(HTTPConsts.CONTENT_TYPE), body)

    def parse_request_string(self, splitted_request_string):
        request_struct = {}

        if len(splitted_request_string) > 0:
            for raw_row in splitted_request_string:
                row = raw_row.split(":")

                if len(row) == 2:
                    request_struct[row[0].upper()] = row[1].strip()

        return request_struct

    def split_request_string(self, string):
        return string.replace("\r", "").split("\n")
