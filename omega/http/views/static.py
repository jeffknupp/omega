"""Module containing code to serve static files."""
import os
from omega.http.utils import make_response, mimetype_for_path


class StaticFileView(object):
    """View class for static file routing."""
    def __call__(self, *args, **kwargs):
        file_path = kwargs['file_path']
        with open(os.path.join('static', file_path), 'r') as file_handle:
            response = make_response(file_handle.read())
            response.headers['Content-type'] = mimetype_for_path(file_path)
            return response
