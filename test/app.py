"""Test the app."""
from whizbang.http.core import create_app
from whizbang.http.resource import json_resource_definition
from whizbang.orm import create_engine
from werkzeug import run_simple

if __name__ == '__main__':
    app = create_app(__name__)
    app.page('/', 'base.html')
    app.engine(create_engine('sqlite+pysqlite:///db.sqlite3'))
    #app.json_resource('tweet', json_resource_definition('tweet'))
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
