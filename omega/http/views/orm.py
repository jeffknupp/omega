"""Module containing code to automatically generate RESTful API from an ORM
model."""
from jinja2 import Environment, PackageLoader
from werkzeug import redirect
from wtforms.ext.sqlalchemy.orm import model_form

from omega.http.utils import make_response


class ORMResourceView(object):
    """Generates a REST API from an ORM model."""

    def __init__(self, name, cls, session):
        self.name = name
        self.cls = cls
        self._session = session()
        self.form = model_form(self.cls, self._session) 
        self.env = Environment(loader=PackageLoader('omega.http.views'))

    def handle_get(self, request, primary_key):
        """Return a response for a get request for a specific resource.

        :param request: The incoming Request object
        :param primary_key: The primary_key of the ORM model to retrieve

        """

        resource = self._session.query(self.cls).get(primary_key)
        if not resource:
            return None
        self.template = self.env.get_template('resource.html')
        form = self.form(request.form, resource)
        return make_response(self.template.render(
            resource=resource, name=self.name, form=form))

    def handle_get_collection(self, request):
        """Return a response for a get request on the entire collection.

        :param request: The incoming Request object.

        """

        resources = self._session.query(self.cls).all()
        self.template = self.env.get_template('resources.html')

        return make_response(
            self.template.render(
                resources=resources, form=self.form(), name=self.cls.__name__))

    def handle_post(self, request, primary_key=None):
        """Return a :class:`werkzeug.Response` object after handling the POST
        call.

        :param request: The incoming Request object.
        :param primary_key: The primary_key of the ORM model to retrieve

        """

        if primary_key:
            print 'pirmary_key'
            resource = self._session.query(self.cls).get(primary_key)
            form = self.form(request.form, obj=resource)
            if form.validate():
                form.populate_obj(resource)
                resource = self._session.merge(resource)
                self._session.commit()
        else:
            print 'cls'
            resource = self.cls()
            form = self.form(request.form, obj=resource)
            form.populate_obj(resource)
            self._session.add(resource)
            self._session.commit()
        return redirect(resource.url())

    def handle_put(self, request, primary_key):
        """Return a :class:`werkzeug.Response` object after handling the PUT
        call.

        :param request: The incoming Request object.
        :param primary_key: The primary_key of the ORM model to retrieve

        """

        resource = self._session.query(self.cls).get(primary_key)
        if resource:
            for field, value in request.form.items():
                setattr(resource, field, value)
        else:
            resource = self.cls(request.form)
        error = self.validate_data(resource)
        if error:
            return None
        self._session.add(resource)
        self._session.commit()

    def handle_patch(self, request, primary_key):
        """Return a :class:`werkzeug.Response` object after handling the PUT
        call.

        :param request: The incoming Request object.
        :param primary_key: The primary_key of the ORM model to retrieve

        """

        resource = self._session.query(self.cls).get(primary_key)
        if resource:
            for field, value in request.form.items():
                setattr(resource, field, value)
        else:
            resource = self.cls(request.form)
        error = self.validate_data(resource)
        if error:
            return None
        self._session.add(resource)
        self._session.commit()
        template = self.env.get_template('resource.html')

        return make_response(template.render(resource=resource))

    def handle_delete(self, request, primary_key):
        """Return a :class:`werkzeug.Response` object after handling
        the DELETE call or a POST to /delete.

        :param request: The incoming Request object.
        :param primary_key: The primary_key of the ORM model to retrieve

        """

        resource = self._session.query(self.cls).get(primary_key)
        self._session.delete(resource)
        self._session.commit()
        return redirect('/' + self.name)

    def validate_data(self, resource):
        """Return an error message if the given resource's data is
        not valid based on our definition.

        :param resource: The resource to be validated

        """
        for name, value in self.cls.__table__.columns.items():
            if getattr(resource, name) != value.type:
                return False
        return True
