class Route:
    def __init__(self, url, handler, methods):
        self.url = url
        self.methods = methods if methods else ["GET"]
        self.handler = handler
