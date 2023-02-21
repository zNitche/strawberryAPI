from strawberry.parsers import request_payload_parsers as parsers
import sys


class RequestPayloadParser:
    def __init__(self):
        self.parsers = {
            parsers.JsonParser.get_content_type(): parsers.JsonParser,
            parsers.FormDataParser.get_content_type(): parsers.FormDataParser,
        }

    def get_parser(self, content_type):
        return self.parsers.get(content_type)

    def parse_payload(self, content_type, payload):
        parser = self.get_parser(content_type)

        if parser:
            try:
                payload = parser.parse(payload)
            except Exception as e:
                print(f"Exception during parsing payload using {parser.get_content_type()}")
                sys.print_exception(e)

        return payload
