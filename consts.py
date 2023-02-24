class HTTPConsts:
    HOST_KEY = "HOST"
    CONTENT_LENGTH = "CONTENT-LENGTH"
    CONTENT_TYPE = "CONTENT-TYPE"

    CONTENT_TYPE_JSON = "application/json"
    CONTENT_TYPE_CSS = "text/css"
    CONTENT_TYPE_HTML = "text/html"
    CONTENT_TYPE_JS = "text/javascript"
    CONTENT_TYPE_FORM_DATA = "application/x-www-form-urlencoded"
    CONTENT_TYPE_TEXT = "text/plain"

    FILES_TYPES_BY_EXTENSION = {
        ".css": CONTENT_TYPE_CSS,
        ".js": CONTENT_TYPE_JS,
        ".html": CONTENT_TYPE_HTML,
        ".txt": CONTENT_TYPE_TEXT,
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


class FormatConsts:
    PATH_ARGUMENT_START = "<"
    PATH_ARGUMENT_END = ">"

    BASE_TEMPLATE_DEFINE = "#EXTEND"

    TEMPLATE_VAR_START = "{{"
    TEMPLATE_VAR_END = "}}"

    TEMPLATE_SECTION_START = "#SECTION"
    TEMPLATE_SECTION_END = "#END"

    TEMPLATE_SECTION_SLOT = "#SECTION_SLOT"


class ServerConsts:
    LED_BLINK_PERIOD_WIFI_CONNECTING = 250
    LED_BLINK_WIFI_CONNECTED = 3000

    WIFI_RECONNECT_PERIOD = 300000
