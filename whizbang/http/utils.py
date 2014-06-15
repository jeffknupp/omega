from werkzeug import Response


def make_response(content):
    """Return a Response object suitable for return."""
    return Response(content, headers={'Content-type': 'text/html'})
