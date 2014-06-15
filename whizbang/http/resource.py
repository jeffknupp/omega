def define_resources(app, resources):
    for name in resources:
        app.register_resource(name, resources[name]['endpoint'])
