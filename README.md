# Omega!

**Omega - The web *platform* that "has an app for that"**

## What is Omega?

Omega is an attempt to bring back innovation to Python web frameworks. Its
goal is to be more than a web framework; Omega aims to be a platform
on which *any* type of web application can be built, batteries included.
That means Omega ships with support for creating ORM-backed CRUD
applications, NoSQL REST APIs, real-time applications using Websockets, and
simple, mostly static page applications.

To this end, Omega will include the tools/libraries listed below. Of course,
it's still in its infancy, so many of the items below are vaporware.

### `search`

Support for full-text search in web applications. *Coming Soon*.

### `kvs`

A pure-Python NoSQL database usable as a backing store for a web application.
*In progress*.

### `queue`

A distributed, asychronous task queue for out-of-band/background task execution in web
applications. Includes support for `cron`-like job scheduling. *In progress.*

### `log/stat`

A centralized logging/metrics server with fully browsable logs and metric
reporting. Includes monitoring for metrics like process uptime, request speed,
number of exceptions, etc. *Coming Soon*

### `settings`

A centralized live-settings server capable of providing service discovery
capabilities as well as a management frontent for traditional database-backed
application settings. *Coming Soon*

### `http`

A micro web framework with macro capabilities. *In progress.*

Here are a few examples of the vastly different types of applications you can already 
build in an instant:

##### ORM-backed CRUD application

`runserver.py`

```python

from omega.http.core import create_app
from omega.http.orm import create_engine
from werkzeug import run_simple
from models import Twoot, User

if __name__ == '__main__':
    app = create_app(__name__)
    app.engine(create_engine('sqlite+pysqlite:///db.sqlite3'))
    app.orm_resource(Twoot)
    app.orm_resource(User)
    app.auto_generate_home()
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)

```

`models.py`

```python

import datetime

from omega.http.orm import Model, Column, String, DateTime, Integer, relationship, ForeignKey

class User(Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    joined_at = Column(DateTime, default=datetime.datetime.now())

    def __str__(self):
        return self.user_name

class Twoot(Model):
    __tablename__ = 'twoot'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    posted_at = Column(DateTime, default=datetime.datetime.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

```

This gives you the following, for free:

###### Homepage

![Home page shot](/images/home.png)

###### List of objects

![Resources shot](/images/resources.png)

By adding a `sockets.py` file with the following contents (and creating a new
route function using the `route` decorator):

```python
from socketio.namespace import BaseNamespace


class ChatNamespace(BaseNamespace):
    sockets = {}

    def on_chat(self, msg):
        self.emit('chat', msg)

    def recv_connect(self):
        self.sockets[id(self)] = self

    def disconnect(self, *args, **kwargs):
        if id(self) in self.sockets:
            del self.sockets[id(self)]
        super(ChatNamespace, self).disconnect(*args, **kwargs)

    @classmethod
    def broadcast(self, event, message):
        for ws in self.sockets.values():
            ws.emit(event, message)
```

(in `runserver.py`):

```python
@app.route('/chat', methods=['POST'])
def chat(request):
    """Route chat posts to the *chat* handler function. Broadcast the message
    to all users."""
    message = '{}: {}'.format(request.form['user'], request.form['message'])
    if message:
        ChatNamespace.broadcast('message', message)
    return Response()
```

You now have free real-time chat that degrades gracefully via socket.io. Connect
two browsers to the root page and type a message in one browser. It will pop up
in the chat area of the other browser.
