from strawberry.routes.blueprint import Blueprint
from strawberry.communication.response import Response
from strawberry.utils import routes_utils
import json


api = Blueprint("api", url_prefix="/api", templates_dir="/routes")


@api.route("/test_api", methods=["GET"])
def test_api(request):
    return Response(200, payload=json.dumps({"test_res": True}))


@api.route("/test_page", methods=["GET"])
def test_page(request):
    print(request.path_parameters)

    context = {
        "test_var": "parsed test var"
    }

    return routes_utils.render_template(api.get_template_path("index.html"), context)


@api.route("/test_forms_page", methods=["GET"])
def test_forms_page(request):
    return routes_utils.render_template(api.get_template_path("forms.html"), {})


@api.route("/form_test", methods=["POST"])
def form_test(request):
    print(f"form request body: {request.body}")
    url = api.current_app.url_for("api.test_page_url_args", path_parameters={"arg_1": request.body.get("name")})

    return routes_utils.redirect(url)


@api.route("/test_page_url_args/<arg_1>", methods=["GET"])
def test_page_url_args(request):
    print(request.path_parameters)

    return Response(200)


@api.route("/test_page_redirect", methods=["GET"])
def test_page_redirect(request):
    url = api.current_app.url_for("api.test_page_url_args", path_parameters={"arg_1": 123})

    return routes_utils.redirect(url)


@api.route("/test_api_error", methods=["POST"])
def test_api_error(request):
    return api.current_app.raise_error(500)


@api.route("/test_api_post", methods=["POST"])
def test_api_post(request):
    response = Response(200)
    response.headers["TEST_TOKEN"] = 123

    return response


@api.route("/test_get_file", methods=["GET"])
def test_get_file(request):
    return routes_utils.send_file("/routes/data/test_data.txt", "test_file.txt", is_file_streamed=True)
