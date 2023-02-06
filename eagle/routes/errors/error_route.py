class ErrorRoute:
    def __init__(self, handler, status_code):
        self.handler = handler
        self.status_code = status_code
