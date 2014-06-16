import os
from jinja2 import Environment, FileSystemLoader
from whizbang.http.utils import make_response, mimetype_for_path


class TemplateView(object):
    """View class for direct-to-template routing."""
    def __init__(self, template_name):
        self.env = Environment(loader=FileSystemLoader('templates'))
        self.template = self.env.get_template(template_name)

    def __call__(self, request):
        return make_response(self.template.render())


class StaticFileView(object):
    """View class for static file routing."""
    def __call__(self, *args, **kwargs):
        file_path = kwargs['file_path']
        with open(os.path.join('static', file_path), 'r') as fh:
            response = make_response(fh.read())
            response.headers['Content-type'] = mimetype_for_path(file_path)
            return response
