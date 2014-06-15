from whizbang.http.core import create_app
from werkzeug import run_simple

if __name__ == '__main__':
    app = create_app(__name__)
    app.page('/', 'base.html')
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
