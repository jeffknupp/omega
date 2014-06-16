import datetime
import json
import re
import uuid

from werkzeug import Response

from whizbang.http.cache import DummyCache
from whizbang.http.utils import make_response
from whizbang.http.resource import DATE


class JSONResourceView(object):
    """View class for JSON-based resource routing."""
    def __init__(self, name, definition):
        self.name = name
        self._definition = definition
        self._cache = DummyCache()
        self._resources = set()

    def __call__(self, request, primary_key=None):
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
                response = Response(
                    self.all_resources(),
                    headers={'Content-type': 'application/json'})
            else:
                response = Response(
                    json.dumps(self._cache[primary_key]),
                    headers={'Content-type': 'application/json'})
            return response

    def handle_POST(self, request):
        """Return a :class:`werkzeug.Response` object after handling the POST
        call."""
        resource = json.loads(request.data)
        error = self.validate_data(resource)
        if error:
            return bad_reqeust(error)
        resource_id = str(uuid.uuid4())
        resource['_id'] = resource_id
        self._resources.add(resource_id)
        self._cache[resource_id] = resource
        return Response(
            json.dumps(to_json(resource)),
            headers={'Content-type': 'application/json'})

    def handle_PUT(self, request, primary_key):
        """Return a :class:`werkzeug.Response` object after handling the PUT
        call."""
        resource = self._cache[primary_key]
        resource.update(json.loads(request.data))
        error = self.validate_data(resource)
        if error:
            return bad_reqeust(error)
        self._cache[primary_key] = resource
        return Response(
            json.dumps(to_json(resource)),
            headers={'Content-type': 'application/json'})

    def handle_PATCH(self, request, primary_key):
        """Return a :class:`werkzeug.Response` object after handling the PUT
        call."""
        resource = self._cache[primary_key]
        resource.update(json.loads(request.data))
        self._cache[primary_key] = resource
        return Response(
            json.dumps(to_json(resource)),
            headers={'Content-type': 'application/json'})

    def handle_DELETE(self, request, pk):
        """Return a :class:`werkzeug.Response` object after handling
        the DELETE call."""
        del self._cache[pk]
        return Response(
            ('204 No Content'), headers={'Content-type': 'application/json'})

    def validate_against_definition(self, fields):
        """Return an error message if there are extra or missing fields on the
        message."""
        defined_fields = set(self._definition.keys())
        if fields - defined_fields:
            return 'Unknown fields [{}]'.format(
                ', '.join([f for f in fields - defined_fields]))
        if defined_fields - fields:
            return 'Missing fields [{}]'.format(
                ', '.join([f for f in defined_fields - fields]))

    def validate_data(self, resource):
        """Return an error message if the given resource's data is
        not valid based on our definition."""
        fields = set(resource.keys())
        error = self.validate_against_definition(fields)
        if error:
            return error
        for field, value in resource.items():
            if field not in self._definition:
                return 'Unknown field [{}]'.format(field)
            if isinstance(value, (str, unicode)):
                match = re.match(DATE, value)
                if match and match.group(0):
                    resource[field] = datetime.datetime.strptime(
                        value, '%Y-%m-%d %H:%M:%S')
                    value = resource[field]
            if not isinstance(value, self._definition[field]['type']):
                return 'Invalid type for field [{}]. Expected [{}]' \
                    'but got [{}]'.format(
                        field,
                        self._definition[field]['type'],
                        type(value))

    def all_resources(self):
        """Return all resources as a list of JSON objects."""
        return json.dumps(
            [to_json(self._cache.get(r)) for r in self._resources])


def to_json(resource):
    """Return the JSON representation of the resource."""
    values = resource
    for field, value in resource.items():
        if isinstance(value, datetime.datetime):
            values[field] = str(value)
    return values


def bad_reqeust(message):
    response = make_response(json.dumps({'status': 'ERR', 'message': message}))
    response.status_code = 400
    return response