import json
import os

from jinja2 import Environment, FileSystemLoader

from whizbang.http.cache import DummyCache
from whizbang.http.utils import make_response

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
            file_name = file_path.split('/')[-1]
            if '.css' in file_name:
                mimetype = 'text/css'
            elif '.js' in file_name:
                mimetype = 'script/js'
            response = make_response(fh.read())
            response.headers['Content-type'] =  mimetype
            return response

class View(object):
    def __init__(self, name, endpoint):
        self.name = name
        self.endpoint = endpoint
        self._resources = set()
        self._cache = DummyCache

    def __call__(self, request):
        if request.path == self.endpoint:
            return self.all_resources()

    def all_resources(self):
        return json.dumps([self._cache.get(r) for r in self._resources])
