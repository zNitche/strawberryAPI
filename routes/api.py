from eagle.routes.blueprint import Blueprint
from eagle.communication.response import Response
from eagle.communication.file_response import FileResponse


api = Blueprint("api", url_prefix="/api")


@api.route("/test_api", methods=["POST"])
def test_api(request):
    return Response(200)


@api.route("/test_page", methods=["GET"])
def test_page(request):
    return FileResponse(file_path="/routes/index.html")
