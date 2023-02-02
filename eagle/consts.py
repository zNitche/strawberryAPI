class HTTPConsts:
    HOST_KEY = "HOST"
    CONTENT_LENGTH = "CONTENT-LENGTH"
    CONTENT_TYPE = "CONTENT-TYPE"

    CONTENT_TYPE_JSON = "application/json"
    CONTENT_TYPE_CSS = "text/css"
    CONTENT_TYPE_HTML = "text/html"


class RequestsConsts:
    pass


class ResponseConsts:
    RESPONSES_STATUSES_MESSAGES = {
        200: "OK",
        500: "Internal Server Error",
        404: "Not Found",
        405: "Method Not Allowed",
        400: "Bad Request",
    }
