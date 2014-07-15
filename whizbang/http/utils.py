"""Utilities for the whizbang http module."""

from werkzeug import Response


def mimetype_for_path(path):
    """Return the Internet Type for the given path.

    :param str path: Path to detect type for

    """

    if '.css' in path:
        return 'text/css'
    elif '.js' in path:
        return 'script/js'


def make_response(content):
    """Return a Response object suitable for return.

    Note: This currently always returns HTML responses. For a JSON response,
    override the Content-type header to be 'application/json'.

    :param content: Content to be returned by the response

    """
    return Response(content, headers={'Content-type': 'text/html'})
