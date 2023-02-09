from strawberry.communication.response import Response
from strawberry.communication.file_response import FileResponse


def redirect(url):
    response = Response(301)
    response.headers["LOCATION"] = url

    return response


def render_template(path, context):
    response = FileResponse(path)

    print(f"file content: {response.file_content}, status code: {response.status_code}")

    return response
