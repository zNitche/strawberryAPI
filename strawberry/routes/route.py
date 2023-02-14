from strawberry.routes.base.route_base import RouteBase


class Route(RouteBase):
    def __init__(self, url, handler, methods):
        super().__init__(handler)

        self.url = url
        self.methods = methods if methods else ["GET"]

        self.path_argument_start = "<"
        self.path_argument_end = ">"

    def get_url_pattern_data(self):
        splitted_url = self.url.split("/")

        if splitted_url[0] == "":
            splitted_url.pop(0)

        url_pattern_data = []

        for url_part in splitted_url:
            is_parameter = True if url_part.startswith(self.path_argument_start) and \
                                   url_part.endswith(self.path_argument_end) else False

            url_pattern_data.append({
                "url_part": url_part,
                "is_parameter": is_parameter
            })

        return url_pattern_data

    def match_bare_url(self, url):
        return True if url == self.url else False

    def match_url_with_parameters(self, url):
        splitted_url = url.split("/")
        splitted_self_url = self.url.split("/")

        if splitted_url[0] == "" and splitted_self_url[0] == "":
            splitted_url.pop(0)
            splitted_self_url.pop(0)

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

    def match_url(self, url):
        if self.path_argument_start in self.url and self.path_argument_end in self.url:
            return self.match_url_with_parameters(url)

        else:
            return self.match_bare_url(url)
