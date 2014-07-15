"""Whizbang's core HTTP module.

Application objects are created by instantiating the 
:class:`whizbang.http.core.WebApplication` class.
"""
from sqlalchemy.orm import sessionmaker

from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug import run_simple

from whizbang.http.views.template import TemplateView
from whizbang.http.views.static import StaticFileView
from whizbang.http.views.nosql import NoSQLResourceView
from whizbang.http.views.orm import ORMResourceView
from whizbang.http.views.generated import GeneratedIndexView
from whizbang.http.orm import Model
from werkzeug.wsgi import SharedDataMiddleware

from socketio.server import SocketIOServer
from socketio import socketio_manage


class WebApplication(object):
    """A WSGI application object responsible for handling requests.

    :param name: The name of the application.
    :param url_map: A map of :class:`werzeug.routing.Rule` objects to endpoint
              names.
    :param debug: True if the application is in debug mode.
    """

    def __init__(self, name):
        """Return a new application object with built-in static file routing
        already setup.
        
        TODO: Make static directory configurable.

        :param str name: The name of the application.
        """
        self.name = name
        self.url_map = Map([Rule('/static/<path:file_path>', endpoint='static')])
        self._routes = {'static': StaticFileView()}
        self._engine = None
        self.debug = None
        self._orm_resources = []
        self._namespaces = {}

    def page(self, endpoint, template_name):
        """Register a template to be served for the specified *endpoint*.

        :param str endpoint: The endpoint (i.e. '/home') this template should be served at.
        :param str template_name: The name of the template to be rendered.
        """
        name = template_name.split('.')[0]
        self.url_map.add(Rule(endpoint, endpoint=name))
        self._routes[name] = TemplateView(template_name)

    def nosql_resource(self, resource):
        """Register a NoSQL resource."""
        self.url_map.add(Rule('/' + resource.name, endpoint=resource.name))
        self.url_map.add(Rule('/' + resource.name + '/<string:primary_key>', endpoint=resource.name))
        self._routes[resource.name] = NoSQLResourceView(resource)

    def orm_resource(self, cls, resource_view_class=ORMResourceView):
        """Register an ORM resource at an endpoint defined by the class's
        *__endpoint__* attribute.

        A reasonably complete set of RESTful endpoints are created/supported,
        with support for all HTTP methods as well as form-based manipulation of
        resources.

        :param cls: The ORM class to register.
        :type cls: :class:`whizbang.http.orm.model.Resource`
        :param resource_view_class: The class to generate the resource's views
                                    from. This should be a subclass of
                                    :class:`whizbang.http.views.orm.ORMResourceView`
        """
        name = cls.endpoint()[1:]
        self._orm_resources.append(name)
        orm_view = resource_view_class(name, cls, self.Session)
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
        """Register a socketio namespace class at the given *endpoint*.

        :param str endpoint: The endpoint (i.e. '/chat') to register.
        :param namespace_class: SocketIO Namespace to register at the
                                given endpoint.
        :type namespace_class: :class:`socketio.namespace.BaseNamespace`
        """
        self._namespaces[endpoint] = namespace_class

    def auto_generate_home(self):
        """Auto-generate an index page that lists all the ORM resources
        registered."""
        self.url_map.add(Rule('/', endpoint='home'))
        self._routes['home'] = GeneratedIndexView(self._orm_resources)

    def route(self, rule, **kwargs):
        """Register *function* to handle requests to *endpoint*.

        :param str endpoint: The endpoint (i.e. `/foo/bar`) to register.
        :param function: The view function to handle requests.
        """
        def decorator(f):
            methods = kwargs.pop('methods', None)
            self.url_map.add(Rule(
                rule,
                endpoint=rule,
                methods=methods,
                *kwargs))
            self._routes[rule] = f
            return f
        return decorator

    def dispatch_request(self, urls, request):
        """Dispatch the incoming *request* to the given view function or class.

        If the "request" is a socket.io message, route it to the registered
        namespace.

        :param urls: The URLs parsed by binding the URL map to the environment.
        :param request: The current HTTP request.
        :type request :class:`werkzeug.Request`:
        """
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
        """Return a response to the request described by *environ*.

        Invokes the application object as a WSGI application and returns an
        HTTP Response.

        :param environ: The current environment variables.
        :param start_response: A callable to provide the response.
        """
        request = Request(environ)
        urls = self.url_map.bind_to_environ(environ)
        response = self.dispatch_request(urls, request)
        return response(environ, start_response)

    def engine(self, engine):
        """Set the application's database engine to be *engine*.

        :param engine: The SQLAlchemy engine object to bind.
        """
        self._engine = engine
        self.Session = sessionmaker(bind=engine)
        Model.metadata.create_all(self._engine)

    def run(self, host='127.0.0.1', port=5000, debug=None):
        """Run the application at the given host and port.

        :param str host: The hostname to run the application on.
        :param int port: The port to run the application on.
        """

        if debug is not None:
            self.debug = debug
        SocketIOServer(
            ('0.0.0.0', 5000),
            SharedDataMiddleware(self, {}),
            resource="socket.io",
            policy_server=False).serve_forever()

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

def create_app(name):
    return WebApplication(name)
