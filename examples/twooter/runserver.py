"""Code for the Twooter application."""
from werkzeug import Response
from omega.http.core import create_app
from sqlalchemy import create_engine
from gevent import monkey
monkey.patch_all()
from models import Twoot, User
from sockets import ChatNamespace


app = create_app(__name__)


@app.route('/chat', methods=['POST'])
def chat(request):
    """Route chat posts to the *chat* handler function. Broadcast the message
    to all users."""
    message = '{}: {}'.format(request.form['user'], request.form['message'])
    if message:
        ChatNamespace.broadcast('message', message)
    return Response()


if __name__ == '__main__':
    # Set the SQLAlchemy database engine
    app.engine(create_engine(
        'postgresql+psycopg2://jknupp@localhost/omega'))
    # Auto-generate an ORM resource view from the given models
    app.orm_resource(Twoot)
    app.orm_resource(User)
    # Create a socketio endpoint for chatting
    app.namespace('/chats', ChatNamespace)
    # Auto generate a home page for the project
    app.auto_generate_home()
    app.run(debug=True)
