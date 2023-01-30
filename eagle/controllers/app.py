class App:
    def __init__(self, requests_handler):
        self.requests_handler = requests_handler

    def run(self):
        self.requests_handler()
