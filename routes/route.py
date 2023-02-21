from strawberry.routes.base.route_base import RouteBase
from strawberry.consts import FormatConsts


class Route(RouteBase):
    def __init__(self, url, handler, methods):
        super().__init__(handler)

        self.url = url
        self.splitted_url = self.split_url(url)
        self.methods = methods if methods else ["GET"]

    def split_url(self, url):
        splitted_url = url.split("/")

        if splitted_url[0] == "":
            splitted_url.pop(0)

        return splitted_url

    def accepts_path_parameters(self):
        return FormatConsts.PATH_ARGUMENT_START in self.url and FormatConsts.PATH_ARGUMENT_END in self.url

    def match_url(self, url):
        match = self.match_url_with_parameters(url) if self.accepts_path_parameters() else self.match_bare_url(url)

        return match

    def match_bare_url(self, url):
        return True if url == self.url else False

    def match_url_with_parameters(self, url):
        splitted_url = self.split_url(url)
        url_data = self.get_url_data()

        lengths_match = True if len(splitted_url) == len(self.splitted_url) else False
        non_empty_parts = True if (("" not in splitted_url) and (" " not in splitted_url)) else False
        pattern_match = True

        if lengths_match:
            for part_id, data in enumerate(url_data):
                splitted_url_part = splitted_url[part_id]

                if (splitted_url_part != data["url_part"]) and not data["is_parameter"]:
                    pattern_match = False
                    break

        return True if (lengths_match and pattern_match and non_empty_parts) else False

    def concat_url_with_parameters(self, parameters):
        url = self.url

        for parameter in parameters:
            parameter_slot_name = f"{FormatConsts.PATH_ARGUMENT_START}{parameter}{FormatConsts.PATH_ARGUMENT_END}"

            parameter_value = parameters.get(parameter)
            parameter_value = str(parameter_value) if parameter_value else parameter_value

            url = url.replace(parameter_slot_name, parameter_value)

        return url

    def get_url_data(self):
        url_data = []

        for url_position, url_part in enumerate(self.splitted_url):
            is_parameter = True if self.is_parameter(url_part) else False

            url_data.append({
                "url_position": url_position,
                "url_part": url_part,
                "is_parameter": is_parameter,
                "parameter_name": url_part[1:-1] if is_parameter else None
            })

        return url_data

    def get_path_parameters_for_url(self, url):
        parameters = {}

        if self.accepts_path_parameters():
            splitted_url = self.split_url(url)

            for data_part in self.get_url_data():
                if data_part["is_parameter"]:
                    parameters[data_part["parameter_name"]] = splitted_url[data_part["url_position"]]

        return parameters

    def is_parameter(self, name):
        return True if name.startswith(FormatConsts.PATH_ARGUMENT_START) and name.endswith(FormatConsts.PATH_ARGUMENT_END) else False
