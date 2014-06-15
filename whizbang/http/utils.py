from werkzeug import Response


def mimetype_for_path(path):
    if '.css' in path:
        return 'text/css'
    elif '.js' in path:
        return 'script/js'

def make_response(content):
    """Return a Response object suitable for return."""
    return Response(content, headers={'Content-type': 'text/html'})
