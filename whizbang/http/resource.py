import os
import json
import re
import datetime

DATE = re.compile("\d+-\d+-\d+ \d+:\d+:\d+")


class NoSQLResource(object):

    def __init__(self, name, store=None):
        self.fields = {}
        self.name = name
        self.store = None
        self._generate_resource_definition()

    def set_store(self, store):
        self.store = store

    def _generate_resource_definition(self):
        with open(os.path.join('resources', self.name + '.js'), 'r') as fh:
            resource_file = json.loads(fh.read())
            for key, value in resource_file.items():
                if value.startswith('#'):
                    self.fields[key] = NoSQLObjectReference(key, NoSQLResource)
                elif isinstance(value, (str, unicode)):
                    match = re.match(DATE, value)
                    if match and match.group(0):
                        self.fields[key] = NoSQLField(key, datetime.datetime, value)
                else:
                    self.fields[key] = NoSQLField(key, datetime.datetime, value)

    def set(self, *args, **kwargs):
        for name in self.fields:
            self.fields[name] = kwargs[name]

    def get(self):
        values = {}
        for name in self.fields:
            values[name] = self.fields[name].get()


class NoSQLField(object):

    def __init__(self, name, field_type, example=None, value=None):
        self.name = name
        self.type = field_type
        self.example = example
        self.value = value

    def example(self):
        print {self.name: self.example}

    def get(self):
        return self.value()


class NoSQLObjectReference(NoSQLField):

    def __init__(self, name, field_type, example=None, value=None):
        self.name = name
        self.type = field_type
        self.example = example
        self.object_id = value

    def get(self, store):
        return store.get((self.type, self.object_id))


def define_resources(app, resources):
    for name in resources:
        app.register_resource(name, resources[name]['endpoint'])
