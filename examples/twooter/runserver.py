"""Code for the Twooter application."""
from werkzeug import Response
from whizbang.http.core import create_app
from whizbang.http.socket_io import ShoutsNamespace

from werkzeug.wsgi import SharedDataMiddleware
from gevent import monkey; monkey.patch_all()

from socketio.server import SocketIOServer

app = create_app(__name__)
app.auto_generate_home()
app.namespace('/shouts', ShoutsNamespace)

def shout(request):
    message = request.args.get('msg', None)
    if message:
        ShoutsNamespace.broadcast('message', message)
        return Response("Message shouted!")
    else:
        return Response("Please specify your message in the 'msg' parameter")

app.route('/shout', shout)

if __name__ == '__main__':
    server = SocketIOServer(('0.0.0.0', 5000), SharedDataMiddleware(app, {}),
        namespace="socket.io", policy_server=False)
    server.serve_forever()
#if __name__ == '__main__':
#    app.engine(create_engine('sqlite+pysqlite:///db.sqlite3'))
#    app.nosql_resource(NoSQLResource('twoot'))
#    app.nosql_resource(NoSQLResource('user'))
#    #app.orm_resource(Twoot)
#    #app.orm_resource(User)
#    #app.auto_generate_home()
#    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)
