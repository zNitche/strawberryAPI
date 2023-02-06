class RequestsRegister:
    from eagle.parsers import request_payload_parsers as parsers

    REQUEST_PARSERS = {
        parsers.JsonParser.get_content_type(): parsers.JsonParser,
    }