import collections
import os
import json
import re
import datetime
import glob

DATE = re.compile("\d+-\d+-\d+ \d+:\d+:\d+")

def nosql_resource_definition(resource_directory):
    resource_definition = collections.defaultdict(dict)
    for file_name in glob.glob(os.path.join(resource_directory, '*.js')):
        with open(file_name, 'r') as fh:
            resource_file = json.loads(fh.read())
            for key, value in resource_file.items():
                if value.startswith('#'):
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
