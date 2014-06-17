from jinja2 import Environment, PackageLoader
from werkzeug import redirect
from wtforms.ext.sqlalchemy.orm import model_form

from whizbang.http.utils import make_response


class ORMResourceView(object):
    def __init__(self, name, cls, session):
        self.name = name
        self.cls = cls
        self.form = model_form(self.cls, db_session=session())
        self._Session = session
        self.env = Environment(loader=PackageLoader('whizbang.http.views'))

    def handle_get(self, request, primary_key):
        session = self._Session()
        resource = session.query(self.cls).get(primary_key)
        if not resource:
            return None
        self.template = self.env.get_template('resource.html')
        return make_response(self.template.render(resource=resource))

    def handle_get_collection(self, request):
        session = self._Session()
        resources = session.query(self.cls).all()
        self.template = self.env.get_template('resources.html')

        return make_response(self.template.render(resources=resources, form=self.form(), name=self.cls.__name__))
        return resources

    def handle_post(self, request):
        """Return a :class:`werkzeug.Response` object after handling the POST
        call."""
        resource = self.cls()
        form = self.form(request.form, resource)
        form.populate_obj(resource)
        session = self._Session()
        session.add(resource)
        session.commit()
        return redirect(resource.url())
        
    def handle_put(self, request, primary_key):
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

    def handle_patch(self, request, primary_key):
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

    def handle_delete(self, request, primary_key):
        """Return a :class:`werkzeug.Response` object after handling
        the DELETE call."""
        session = self._Session()
        resource = session.query(self.cls).get(primary_key)
        session.delete(resource)
        session.commit()
        resources = session.query(self.cls).all(primary_key)
        self.template = self.env.get_template('resources.html')

        return make_response(self.template.render(resources=resources))
