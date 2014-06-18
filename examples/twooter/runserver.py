"""Code for the Twooter application."""
from whizbang.http.core import create_app
from whizbang.http.resource import nosql_resource_definitions
from whizbang.http.orm import create_engine
from werkzeug import run_simple
from models import Twoot, User

if __name__ == '__main__':
    app = create_app(__name__)
    app.engine(create_engine('sqlite+pysqlite:///db.sqlite3'))
    app.nosql_resources(nosql_resource_definitions('resources'))
    #app.orm_resource(Twoot)
    #app.orm_resource(User)
    #app.auto_generate_home()
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
