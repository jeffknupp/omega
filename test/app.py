from whizbang.http.core import create_app
from whizbang.http.resource import resource_definition
from werkzeug import run_simple

if __name__ == '__main__':
    app = create_app(__name__)
    app.page('/', 'base.html')
    app.resource('tweet', resource_definition('tweet'))
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
