from jinja2 import Environment, PackageLoader
from wtforms.ext.sqlalchemy.orm import model_form

from whizbang.http.utils import make_response


class ORMResourceView(object):
    def __init__(self, name, cls, session):
        self.name = name
        self.cls = cls
        self.form = model_form(self.cls, db_session=session())
        self._Session = session
        self.env = Environment(loader=PackageLoader('whizbang.http.views'))

    def __call__(self, request, primary_key=None):
        print 'here'
        if request.method == 'POST':
            return self.handle_POST(request)
        elif request.method == 'PUT':
            return self.handle_PUT(request, primary_key)
        elif request.method == 'PATCH':
            return self.handle_PATCH(request, primary_key)
        elif request.method == 'DELETE':
            return self.handle_DELETE(request, primary_key)
        elif request.method == 'HEAD':
            return self.handle_HEAD(request)
        elif request.method == 'OPTIONS':
            return self.handle_OPTIONS(request)

        elif request.method == 'GET':
            if not primary_key:
                session = self._Session()
                resources = session.query(self.cls).all()
                self.template = self.env.get_template('resources.html')

                return make_response(self.template.render(resources=resources, form=self.form(), name=self.cls.__name__))
                return resources
            else:
                session = self._Session()
                resource = session.query(self.cls).get(primary_key)
                self.template = self.env.get_template('resource.html')

                return make_response(self.template.render(resource=resource))

    def handle_POST(self, request):
        """Return a :class:`werkzeug.Response` object after handling the POST
        call."""
        resource = self.cls()
        form = self.form(request.form, resource)
        form.populate_obj(resource)
        session = self._Session()
        session.add(resource)
        session.commit()
        self.template = self.env.get_template('resource.html')

        return make_response(self.template.render(resource=resource))

    def handle_PUT(self, request, primary_key):
        """Return a :class:`werkzeug.Response` object after handling the PUT
        call."""
        session = self._Session()
        resource = session.query(self.cls).get(primary_key)
        if resource:
            for field, value in request.form.items():
                setattr(resource, field, value)
        else:
            resource = self.cls(request.form)
        error = self.validate_data(resource)
        if error:
            return None
        session.add(resource)
        session.commit()
        self.template = self.env.get_template('resource.html')

        return make_response(self.template.render(resource=resource))

    def handle_PATCH(self, request, primary_key):
        """Return a :class:`werkzeug.Response` object after handling the PUT
        call."""
        session = self._Session()
        resource = session.query(self.cls).get(primary_key)
        if resource:
            for field, value in request.form.items():
                setattr(resource, field, value)
        else:
            resource = self.cls(request.form)
        error = self.validate_data(resource)
        if error:
            return None
        session.add(resource)
        session.commit()
        self.template = self.env.get_template('resource.html')

        return make_response(self.template.render(resource=resource))

    def handle_DELETE(self, request, primary_key):
        """Return a :class:`werkzeug.Response` object after handling
        the DELETE call."""
        session = self._Session()
        resource = session.query(self.cls).get(primary_key)
        session.delete(resource)
        session.commit()
        resources = session.query(self.cls).all(primary_key)
        self.template = self.env.get_template('resources.html')

        return make_response(self.template.render(resources=resources))
