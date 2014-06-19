"""Code for the Twooter application."""
from whizbang.http.core import create_app
import werkzeug.serving

import werkzeug.serving
from gevent import monkey
from socketio.server import SocketIOServer

app = create_app(__name__)
monkey.patch_all()

app.auto_generate_home()

@werkzeug.serving.run_with_reloader
def run_dev_server():
    app.debug = True
    port = 6020
    SocketIOServer(('', port), app, resource="socket.io").serve_forever()
