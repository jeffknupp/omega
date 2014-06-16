import datetime
import json
import os
import re
import uuid

from jinja2 import Environment, FileSystemLoader
from werkzeug import Response

from whizbang.http.cache import DummyCache
from whizbang.http.utils import make_response, mimetype_for_path
from whizbang.http.resource import DATE

class TemplateView(object):
    def __init__(self, template_name):
        self.env = Environment(loader=FileSystemLoader('templates'))
        self.template = self.env.get_template(template_name)
    
    def __call__(self, request):
        return make_response(self.template.render())

class StaticFileView(object):

    def __call__(self, *args, **kwargs):
        file_path = kwargs['file_path']
        with open(os.path.join('static', file_path), 'r') as fh:
            response = make_response(fh.read())
            response.headers['Content-type'] =  mimetype_for_path(file_path)
            return response

class ResourceView(object):
    def __init__(self, name, definition):
        self.name = name
        self._definition = definition
        self._cache = DummyCache()
        self._resources = set()

    def __call__(self, request, pk=None):
        if request.method == 'POST':
            return self._handle_POST(request)
        elif request.method == 'PUT':
            return self._handle_PUT(request, pk)
        elif request.method == 'PATCH':
            return self._handle_PATCH(request, pk)
        elif request.method == 'DELETE':
            return self._handle_DELETE(request, pk)
        elif request.method == 'HEAD':
            return self._handle_HEAD(request)
        elif request.method == 'OPTIONS':
            return self._handle_OPTIONS(request)

        elif request.method == 'GET':
            if not pk:
                response = Response(
                    self.all_resources(),
                    headers={'Content-type': 'application/json'})
            else:
                response = Response(
                    json.dumps(self._cache[pk]),
                    headers={'Content-type': 'application/json'})
            return response

    def _handle_POST(self, request):
        resource = json.loads(request.data)
        error = self._validate_data(resource)
        if error:
            return bad_reqeust(error)
        resource_id = str(uuid.uuid4())
        resource['_id'] = resource_id
        self._resources.add(resource_id)
        self._cache[resource_id] = resource
        return Response(
            json.dumps(self._to_json(resource)),
            headers={'Content-type': 'application/json'})

    def _handle_PUT(self, request, pk):
        resource = self._cache[pk]
        resource.update(json.loads(request.data))
        error = self._validate_data(resource)
        if error:
            return bad_reqeust(error)
        self._cache[pk] = resource
        return Response(
            json.dumps(self._to_json(resource)),
            headers={'Content-type': 'application/json'})


    def _validate_against_definition(self, fields):
        defined_fields = set(self._definition.keys())
        if fields - defined_fields:
            return 'Unknown fields [{}]'.format(
                ', '.join([f for f in fields -  defined_fields]))
        if defined_fields - fields:
            return 'Missing fields [{}]'.format(
                ', '.join([f for f in defined_fields - fields]))

    def _validate_data(self, resource):
        fields = set(resource.keys())
        error = self._validate_against_definition(fields)
        if error:
            return error
        for field, value in resource.items():
            if field not in self._definition:
                return 'Unknown field [{}]'.format(field)
            if isinstance(value, (str, unicode)):
                match = re.match(DATE, value)
                if match and match.group(0):
                    resource[field] = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                    value = resource[field]
            if not isinstance(value, self._definition[field]['type']):
                return 'Invalid type for field [{}]. Expected [{}] but got [{}]'.format(
                    field,
                    self._definition[field]['type'],
                    type(value))

    def _to_json(self, resource):
        values = resource
        for field, value in resource.items():
            if isinstance(value, datetime.datetime):
                values[field] = str(value)
        return values

    def all_resources(self):
        return json.dumps([self._to_json(self._cache.get(r)) for r in self._resources])

def bad_reqeust(message):
    response = make_response(json.dumps({'status': 'ERR', 'message': message}))
    response.status_code = 400
    return response
