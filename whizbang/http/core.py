from sqlalchemy.orm import sessionmaker

from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug import run_simple

from whizbang.http.views.template import TemplateView
from whizbang.http.views.static import StaticFileView
from whizbang.http.views.nosql import NoSQLResourceView
from socketio.namespace import BaseNamespace
from whizbang.http.views.orm import ORMResourceView
from whizbang.http.views.generated import GeneratedIndexView
from whizbang.http.orm import Model

from socketio import socketio_manage

class WebApplication(object):
    def __init__(self, name):
        self.name = name
        self.url_map = Map([Rule('/static/<path:file_path>', endpoint='static')])
        self._routes = {'static': StaticFileView()}
        self._engine = None
        self.debug = None
        self.config = {'SERVER_NAME': 'localhost'}
        self._orm_resources = []
        self._namespaces = {}

    def page(self, endpoint, template_name):
        name = template_name.split('.')[0]
        self.url_map.add(Rule(endpoint, endpoint=name))
        self._routes[name] = TemplateView(template_name)

    def nosql_resource(self, resource):
        self.url_map.add(Rule('/' + resource.name, endpoint=resource.name))
        self.url_map.add(Rule('/' + resource.name + '/<string:primary_key>', endpoint=resource.name))
        self._routes[resource.name] = NoSQLResourceView(resource)

    def orm_resource(self, cls):
        name = cls.endpoint()[1:]
        self._orm_resources.append(name)
        orm_view = ORMResourceView(name, cls, self.Session)
        self.url_map.add(Rule('/' + name, endpoint='get_{}s'.format(name), methods=['GET']))
        self.url_map.add(Rule('/' + name, endpoint='post_{}'.format(name), methods=['POST']))
        self.url_map.add(Rule('/' + name + '/<string:primary_key>', endpoint='get_{}'.format(name), methods=['GET']))
        self.url_map.add(Rule('/' + name + '/<string:primary_key>', endpoint='put_{}'.format(name), methods=['PUT']))
        self.url_map.add(Rule('/' + name + '/<string:primary_key>', endpoint='patch_{}'.format(name), methods=['PATCH']))
        self.url_map.add(Rule('/' + name + '/<string:primary_key>', endpoint='delete_{}'.format(name), methods=['DELETE']))
        self.url_map.add(Rule('/' + name + '/<string:primary_key>/delete', endpoint='delete_{}'.format(name), methods=['POST']))
        self.url_map.add(Rule('/' + name + '/<string:primary_key>/edit', endpoint='post_{}'.format(name), methods=['POST']))
        self._routes['get_{}s'.format(name)] = orm_view.handle_get_collection
        self._routes['get_{}'.format(name)] = orm_view.handle_get
        self._routes['put_{}'.format(name)] = orm_view.handle_put
        self._routes['patch_{}'.format(name)] = orm_view.handle_patch
        self._routes['delete_{}'.format(name)] = orm_view.handle_delete
        self._routes['post_{}'.format(name)] = orm_view.handle_post

    def namespace(self, endpoint, namespace_class):
        self._namespaces[endpoint] = namespace_class

    def auto_generate_home(self):
        self.url_map.add(Rule('/', endpoint='home'))
        self._routes['home'] = GeneratedIndexView(self._orm_resources)

    def route(self, endpoint, function):
        self.url_map.add(Rule(endpoint, endpoint=endpoint))
        self._routes[endpoint] = function

    def dispatch_request(self, urls, request):
        if request.path.startswith('/socket.io'):
            try:
                socketio_manage(request.environ, self._namespaces, request)
            except:
                print("Exception while handling socketio connection")
            return Response()
        else:
            response = urls.dispatch(
            lambda e, v: self._routes[e](
                    request, **v))
            if isinstance(response, (unicode, str)):
                headers = {'Content-type': 'text/html'}
                response = Response(response, headers=headers)
            if not response:
                headers = {'Content-type': 'text/html'}
                response = Response('404 Not Found', headers=headers)
                response.status_code = 404
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

    def run(self, host='127.0.0.1', port=5000):
        run_simple(host, port, self, use_debugger=True, use_reloader=True)
    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

def create_app(name):
    return WebApplication(name)
