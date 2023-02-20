from strawberry.routes.blueprint import Blueprint
from strawberry.communication.response import Response
import json


api = Blueprint("api", url_prefix="/api")


@api.route("/error", methods=["POST"])
def error(request):
    return api.current_app.raise_error(500)


@api.route("/post", methods=["POST"])
def post(request):
    response = Response(200)
    response.headers["TEST_TOKEN"] = 123

    return response


@api.route("/get", methods=["GET"])
def get(request):
    return Response(200, payload=json.dumps({"test_res": True}))
