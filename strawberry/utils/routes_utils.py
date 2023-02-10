from strawberry.communication.response import Response
from strawberry.communication.file_response import FileResponse
from strawberry.parsers.template_parser import TemplateParser
from strawberry.utils import files_utils


def redirect(url):
    response = Response(301)
    response.headers["LOCATION"] = url

    return response


def render_template(path, context):
    template_parser = TemplateParser()

    file_content = files_utils.get_file_content(path)
    file_content = template_parser.parse_template(file_content, context)

    response = FileResponse(file_content=file_content)

    print(f"file content: {response.file_content}, status code: {response.status_code}")

    return response
