from eagle.communication.response import Response


def redirect(url):
    response = Response(301)
    response.headers["LOCATION"] = url

    return response
