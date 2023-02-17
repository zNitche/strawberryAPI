from strawberry.consts import HTTPConsts
from strawberry.communication.response import Response
from strawberry.utils import files_utils


class FileResponse(Response):
    def __init__(self, file_path="", file_content=None, content_type=None, status_code=200):
        self.file_path = file_path

        super().__init__()

        self.payload = self.process_file() if file_content is None else file_content
        self.content_type = self.get_content_type_by_extension() if content_type is None else content_type
        self.status_code = status_code

    def get_content_type_by_extension(self):
        file_extension = f".{self.file_path.split('.')[-1]}"
        content_type_from_consts = HTTPConsts.FILES_TYPES_BY_EXTENSION.get(file_extension)

        return content_type_from_consts if content_type_from_consts is not None else HTTPConsts.CONTENT_TYPE_HTML

    def get_file_content(self):
        return files_utils.get_file_content(self.file_path)

    def process_file(self):
        file_content = self.get_file_content()
        self.status_code = self.status_code if file_content != "" else 404

        return file_content

    def get_body(self):
        return self.payload
