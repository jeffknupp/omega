"""Module for creating views that simply render a template."""

from jinja2 import Environment, FileSystemLoader
from omega.http.utils import make_response


class TemplateView(object):
    """View class for direct-to-template routing."""
    def __init__(self, template_name):
        self.env = Environment(loader=FileSystemLoader('templates'))
        self.template = self.env.get_template(template_name)

    def __call__(self, request):
        return make_response(self.template.render())
