from eagle.consts import HTTPConsts
from eagle.communication.response import Response
from eagle.utils import files_utils


class FileResponse(Response):
    def __init__(self, file_path):
        self.file_path = file_path

        super().__init__(content_type=self.get_content_type_by_file_extension())

    def get_content_type_by_file_extension(self):
        file_extension = f".{self.file_path.split('.')[-1]}"

        content_type = HTTPConsts.CONTENT_TYPE_HTML
        content_type_from_consts = HTTPConsts.FILES_TYPES_BY_EXTENSION.get(file_extension)

        return content_type_from_consts if content_type_from_consts is not None else content_type

    def get_file_content(self):
        file_content = ""

        if files_utils.check_if_file_exists(self.file_path):
            with open(self.file_path, "r") as file:
                file_content = file.read()

        return file_content

    def process_file(self):
        file_content = self.get_file_content()
        self.status_code = 200 if file_content != "" else 404

        return file_content

    def get_body(self):
        return self.process_file()
