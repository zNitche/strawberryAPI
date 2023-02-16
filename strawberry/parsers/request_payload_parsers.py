from strawberry.consts import HTTPConsts
import json


class ParserBase:
    @staticmethod
    def get_content_type():
        return None

    @staticmethod
    def parse(data):
        return data


class JsonParser(ParserBase):
    @staticmethod
    def get_content_type():
        return HTTPConsts.CONTENT_TYPE_JSON

    @staticmethod
    def parse(data):
        return json.loads(data)


class FormDataParser(ParserBase):
    @staticmethod
    def get_content_type():
        return HTTPConsts.CONTENT_TYPE_FORM_DATA

    @staticmethod
    def parse(data):
        parsed_data = {}

        for row in data.split("&"):
            splitted_row = row.replace("+", " ").split("=")
            parsed_data[splitted_row[0]] = splitted_row[1]

        return parsed_data
