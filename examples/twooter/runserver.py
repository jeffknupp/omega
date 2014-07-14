"""Code for the Twooter application."""
from werkzeug import Response
from whizbang.http.core import create_app
from sqlalchemy import create_engine
from gevent import monkey
monkey.patch_all()
from models import Twoot, User
from sockets import ChatNamespace


app = create_app(__name__)

@app.route('/chat', methods=['POST'])
def chat(request):
    message = request.form['message']
    if message:
        ChatNamespace.broadcast('message', message)
    return Response()


if __name__ == '__main__':
    engine = create_engine('postgresql+psycopg2://jknupp@localhost/whizbang')
    app.engine(engine)
    app.orm_resource(Twoot)
    app.orm_resource(User)
    app.namespace('/chats', ChatNamespace)
    app.auto_generate_home()
    app.run(debug=True)
