from jinja2 import Environment, PackageLoader
from whizbang.http.utils import make_response


class GeneratedIndexView(object):

    def __init__(self, routes):
        self.routes = routes
        self.env = Environment(loader=PackageLoader('whizbang.http.views'))
        self.template = self.env.get_template('index.html')

    def __call__(self, request):
        return make_response(self.template.render(routes=self.routes))
