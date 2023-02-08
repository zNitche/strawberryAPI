class HTTPConsts:
    HOST_KEY = "HOST"
    CONTENT_LENGTH = "CONTENT-LENGTH"
    CONTENT_TYPE = "CONTENT-TYPE"

    CONTENT_TYPE_JSON = "application/json"
    CONTENT_TYPE_CSS = "text/css"
    CONTENT_TYPE_HTML = "text/html"
    CONTENT_TYPE_JS = "text/javascript"

    FILES_TYPES_BY_EXTENSION = {
        ".css": CONTENT_TYPE_CSS,
        ".js": CONTENT_TYPE_JS,
        ".html": CONTENT_TYPE_HTML
    }


class ResponseConsts:
    RESPONSES_STATUSES_MESSAGES = {
        200: "OK",
        500: "Internal Server Error",
        404: "Not Found",
        405: "Method Not Allowed",
        400: "Bad Request",
        301: "Moved Permanently",
    }
