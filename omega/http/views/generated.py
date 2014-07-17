"""Module responsible for generating an "index" view (root page, or home page,
view) from available routes."""
from jinja2 import Environment, PackageLoader
from omega.http.utils import make_response


class GeneratedIndexView(object):
    """A view that renders the index.html template with all the registered
    routes as context data."""
    def __init__(self, routes):
        self.routes = routes
        self.env = Environment(loader=PackageLoader('omega.http.views'))
        self.template = self.env.get_template('index.html')

    def __call__(self, request):
        return make_response(self.template.render(routes=self.routes))
