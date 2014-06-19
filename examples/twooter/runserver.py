"""Code for the Twooter application."""
from whizbang.http.core import create_app
from whizbang.http.resource import NoSQLResource
from whizbang.http.orm import create_engine
from werkzeug import run_simple

if __name__ == '__main__':
    app = create_app(__name__)
    app.engine(create_engine('sqlite+pysqlite:///db.sqlite3'))
    app.nosql_resource(NoSQLResource('twoot'))
    app.nosql_resource(NoSQLResource('user'))
    #app.orm_resource(Twoot)
    #app.orm_resource(User)
    #app.auto_generate_home()
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
