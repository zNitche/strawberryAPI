from strawberry.routes.base.route_base import RouteBase


class Route(RouteBase):
    def __init__(self, url, handler, methods):
        super().__init__(handler)

        self.url = url
        self.methods = methods if methods else ["GET"]

        self.path_argument_start = "<"
        self.path_argument_end = ">"

    def split_url(self, url):
        splitted_url = url.split("/")

        if splitted_url[0] == "":
            splitted_url.pop(0)

        return splitted_url

    def concat_url_with_parameters(self, parameters):
        url = self.url

        for parameter in parameters:
            parameter_slot_name = f"{self.path_argument_start}{parameter}{self.path_argument_end}"

            parameter_value = parameters.get(parameter)
            parameter_value = str(parameter_value) if parameter_value else parameter_value

            url = url.replace(parameter_slot_name, parameter_value)

        return url

    def get_url_pattern_data(self):
        splitted_url = self.split_url(self.url)
        url_pattern_data = []

        for url_position, url_part in enumerate(splitted_url):
            is_parameter = True if url_part.startswith(self.path_argument_start) and \
                                   url_part.endswith(self.path_argument_end) else False

            url_pattern_data.append({
                "url_position": url_position,
                "url_part": url_part,
                "is_parameter": is_parameter
            })

        return url_pattern_data

    def get_path_parameter_name_by_position(self, url_position):
        splitted_url = self.split_url(self.url)
        parameter_name = None

        if url_position < len(splitted_url):
            url_item = splitted_url[url_position]

            parameter_name = url_item.replace(self.path_argument_start, "").replace(self.path_argument_end, "")

        return parameter_name

    def match_bare_url(self, url):
        return True if url == self.url else False

    def match_url_with_parameters(self, url):
        splitted_url = self.split_url(url)
        splitted_self_url = self.split_url(self.url)

        url_pattern_data = self.get_url_pattern_data()

        lengths_match = True if len(splitted_url) == len(splitted_self_url) else False
        non_empty_parts = True if (("" not in splitted_url) and (" " not in splitted_url)) else False
        pattern_match = True

        if lengths_match:
            for part_id, url_pattern in enumerate(url_pattern_data):
                splitted_url_part = splitted_url[part_id]

                if (splitted_url_part != url_pattern["url_part"]) and not url_pattern["is_parameter"]:
                    pattern_match = False
                    break

        return True if (lengths_match and pattern_match and non_empty_parts) else False

    def accepts_path_parameters(self):
        return self.path_argument_start in self.url and self.path_argument_end in self.url

    def match_url(self, url):
        match = self.match_url_with_parameters(url) if self.accepts_path_parameters() else self.match_bare_url(url)

        return match

    def get_path_parameters_for_url(self, url):
        parameters = {}

        if self.accepts_path_parameters():
            url_pattern_data = self.get_url_pattern_data()
            splitted_url = self.split_url(url)

            for data_part in url_pattern_data:
                if data_part["is_parameter"]:
                    url_position = data_part["url_position"]
                    parameter_name = self.get_path_parameter_name_by_position(url_position)

                    if parameter_name and url_position < len(splitted_url):
                        parameters[parameter_name] = splitted_url[url_position]

        return parameters
