from sqlalchemy.orm import sessionmaker

from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule

from whizbang.http.views.template import TemplateView
from whizbang.http.views.static import StaticFileView
from whizbang.http.views.nosql import NoSQLResourceView
from whizbang.http.views.orm import ORMResourceView
from whizbang.http.orm import Model


class WebApplication(object):
    def __init__(self, name):
        self.name = name
        self.url_map = Map([Rule('/static/<path:file_path>', endpoint='static')])
        self._routes = {'static': StaticFileView()}
        self._engine = None

    def page(self, endpoint, template_name):
        name = template_name.split('.')[0]
        self.url_map.add(Rule(endpoint, endpoint=name))
        self._routes[name] = TemplateView(template_name)

    def nosql_resource(self, name, resource):
        self.url_map.add(Rule('/' + name, endpoint=name))
        self.url_map.add(Rule('/' + name + '/<string:primary_key>', endpoint=name))
        self._routes[name] = NoSQLResourceView(name, resource)

    def orm_resource(self, name, cls):
        self.url_map.add(Rule('/' + name, endpoint=name))
        self.url_map.add(Rule('/' + name + '/<string:primary_key>', endpoint=name))
        self._routes[name] = ORMResourceView(name, cls, self.Session)

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

    def engine(self, engine):
        self._engine = engine
        self.Session = sessionmaker(bind=engine)
        Model.metadata.create_all(self._engine)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

def create_app(name):
    return WebApplication(name)
