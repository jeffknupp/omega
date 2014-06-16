import os
from whizbang.http.utils import make_response, mimetype_for_path

class StaticFileView(object):
    """View class for static file routing."""
    def __call__(self, *args, **kwargs):
        file_path = kwargs['file_path']
        with open(os.path.join('static', file_path), 'r') as fh:
            response = make_response(fh.read())
            response.headers['Content-type'] = mimetype_for_path(file_path)
            return response
