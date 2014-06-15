import json
import os
import uuid

from jinja2 import Environment, FileSystemLoader

from whizbang.http.cache import DummyCache
from whizbang.http.utils import make_response, mimetype_for_path

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

    def __call__(self, request):
        if request.method == 'POST':
            resource = json.loads(request.data)
            error = self._validate_data(resource)
            if error:
                return bad_reqeust(error)
            resource_id = str(uuid.uuid4())
            resource['_id'] = resource_id
            self._resources.add(resource_id)
            self._cache[resource_id] = resource
        if request.path == '/' + self.name:
            return self.all_resources()

    def _validate_data(self, resource):
        fields = set(resource.keys())
        defined_fields = set(self._definition.keys())
        if fields - defined_fields:
            return 'Unknown fields: [{}]'.format(', '.join([f for f in fields -  defined_fields]))
        if defined_fields - fields:
            return 'Missing fields [{}]'.format(', '.join([f for f in defined_fields - fields]))
        for field, value in resource.items():
            if field not in self._definition:
                return 'Unknown field [{}]'.format(field)
            if not isinstance(value, self._definition[field]['type']):
                return 'Invalid type for field [{}]. Expected [{}] but got [{}]'.format(
                    field,
                    self._definition[field]['type'],
                    type(value))

    def all_resources(self):
        return json.dumps([self._cache.get(r) for r in self._resources])

def bad_reqeust(message):
    response = make_response(json.dumps({'status': 'ERR', 'message': message}))
    response.status_code = 400
    return response
