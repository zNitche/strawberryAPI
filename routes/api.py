from eagle.routes.blueprint import Blueprint
from eagle.communication.response import Response
from eagle.communication.file_response import FileResponse
from main import app
import json


api = Blueprint("api", url_prefix="/api")


@api.route("/test_api", methods=["GET"])
def test_api(request):
    return Response(200, payload=json.dumps({"test_res": True}))


@api.route("/test_api_error", methods=["POST"])
def test_api_error(request):
    return app.raise_error(500)


@api.route("/test_page", methods=["GET"])
def test_page(request):
    return FileResponse(file_path="/routes/index.html")
