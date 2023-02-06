from eagle.routes.blueprint import Blueprint
from eagle.communication.response import Response


api = Blueprint("api", url_prefix="api/")


@api.route("/test_api", methods=["POST"])
def test_api(request):
    return Response(200)
