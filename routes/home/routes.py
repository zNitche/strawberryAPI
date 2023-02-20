from strawberry.routes.blueprint import Blueprint
from strawberry.utils import routes_utils


home = Blueprint("home", templates_dir="/routes/home/templates")


@home.route("/", methods=["GET"])
def home_page(request):
    app = home.current_app

    context = {
        "basic_page_url": app.url_for("home.basic_page"),
        "form_page_url": app.url_for("home.form_page"),
        "url_parth_params_url": app.url_for("home.page_url_params", path_parameters={"arg_1": "test_path_param"}),
        "download_file_url": app.url_for("home.get_file")
    }

    return routes_utils.render_template(home.get_template_path("index.html"), context)


@home.route("/basic_page", methods=["GET"])
def basic_page(request):
    context = {
        "test_var": "parsed test var"
    }

    return routes_utils.render_template(home.get_template_path("basic_page.html"), context)


@home.route("/form_page", methods=["GET"])
def form_page(request):
    return routes_utils.render_template(home.get_template_path("form_page.html"), {})


@home.route("/form_post", methods=["POST"])
def form_post(request):
    url = home.current_app.url_for("home.page_url_params", path_parameters={"arg_1": request.body.get("name")})

    return routes_utils.redirect(url)


@home.route("/page_url_params/<arg_1>", methods=["GET"])
def page_url_params(request):
    context = {
        "param": request.path_parameters.get("arg_1")
    }

    return routes_utils.render_template(home.get_template_path("url_params_page.html"), context)


@home.route("/get_file", methods=["GET"])
def get_file(request):
    return routes_utils.send_file("/routes/data/test_data.txt", "test_file.txt", is_file_streamed=True)
