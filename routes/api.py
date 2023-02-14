from strawberry.routes.blueprint import Blueprint
from strawberry.communication.response import Response
from strawberry.utils import routes_utils
from main import app
import json


api = Blueprint("api", url_prefix="/api", templates_dir="/routes")


@api.route("/test_api", methods=["GET"])
def test_api(request):
    return Response(200, payload=json.dumps({"test_res": True}))


@api.route("/test_page", methods=["GET"])
def test_page(request):
    context = {
        "test_var": "parsed test var"
    }

    return routes_utils.render_template(api.get_template_path("index.html"), context)


@api.route("/test_page_url_args/<arg_1>", methods=["GET"])
def test_page_url_args(request):
    return Response(200)


@api.route("/test_page_redirect", methods=["GET"])
def test_page_redirect(request):
    url = app.url_for("api.test_page")

    return routes_utils.redirect(url)


@api.route("/test_api_error", methods=["POST"])
def test_api_error(request):
    return app.raise_error(500)


@api.route("/test_api_post", methods=["POST"])
def test_api_post(request):
    response = Response(200)
    response.headers["TEST_TOKEN"] = 123

    return response
