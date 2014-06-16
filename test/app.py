"""Test the app."""
from whizbang.http.core import create_app
from whizbang.http.resource import json_resource_definition
from whizbang.http.orm import create_engine
from werkzeug import run_simple
from resources.models import Tweet, User

if __name__ == '__main__':
    app = create_app(__name__)
    app.page('/', 'base.html')
    app.engine(create_engine('sqlite+pysqlite:///db.sqlite3'))
    #app.json_resource('tweet', json_resource_definition('tweet'))
    app.orm_resource('tweet', Tweet)
    app.orm_resource('user', User)
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
