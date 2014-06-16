import collections
import os
import json
import re
import datetime

DATE = re.compile("\d+-\d+-\d+ \d+:\d+:\d+")


def json_resource_definition(resource_name):
    resource_definition = collections.defaultdict(dict)
    with open(os.path.join('resources', resource_name + '.js')) as fh:
        resource_file = json.loads(fh.read())
        for key, value in resource_file.items():
            resource_definition[key]['example'] = value
            resource_definition[key]['type'] = type(value)
            if isinstance(value, (str, unicode)):
                match = re.match(DATE, value)
                if match and match.group(0):
                    resource_definition[key]['type'] = datetime.datetime
    return resource_definition


def define_resources(app, resources):
    for name in resources:
        app.register_resource(name, resources[name]['endpoint'])
