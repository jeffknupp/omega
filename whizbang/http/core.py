from werkzeug.wrappers import Request, Response
from whizbang.http.views import TemplateView, StaticFileView, ResourceView
from werkzeug.routing import Map, Rule

class WebApplication(object):
    def __init__(self, name):
        self.name = name
        self.url_map = Map([Rule('/static/<path:file_path>', endpoint='static')])
        self._routes = {'static': StaticFileView()}

    def page(self, endpoint, template_name):
        name = template_name.split('.')[0]
        self.url_map.add(Rule(endpoint, endpoint=name))
        self._routes[name] = TemplateView(template_name)

    def resource(self, name, resource):
        self.url_map.add(Rule('/' + name, endpoint=name))
        self.url_map.add(Rule('/' + name + '/<string:pk>', endpoint=name))
        self._routes[name] = ResourceView(name, resource)

    def dispatch_request(self, urls, request):
        response = urls.dispatch(
            lambda e, v: self._routes[e](
                request, **v))
        if isinstance(response, (unicode, str)):
            headers = {'Content-type': 'text/html'}
            response = Response(response, headers=headers)
        if not response:
            response = Response('404 Not Found')
        return response

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        urls = self.url_map.bind_to_environ(environ)
        response = self.dispatch_request(urls, request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

def create_app(name):
    return WebApplication(name)
