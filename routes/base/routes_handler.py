class RoutesHandler:
    def __init__(self, name, templates_dir=""):
        self.current_app = None

        self.name = name
        self.templates_dir = templates_dir

        self.routes = []

    def get_template_path(self, template_name):
        return f"{self.templates_dir}/{template_name}"

    def set_app(self, app):
        self.current_app = app
