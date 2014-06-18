# Whizbang!

**Whizbang - The web *platform* that "has an app for that"

## What is Whizbang?

Whizbang is an attempt to bring back innovation to Python web frameworks. Its
goal is to be more than a web framework; Whizbang aims to be a platform
on which *any* type of web application can be built, with batteries included.
That means Whizbang ships with support for creating ORM-backed CRUD
applications, NoSQL REST APIs, real-time applications using Websockets, and
simple, mostly static page applications.

To this end, Whizbang includes the following tools/libraries:

### `http`

A micro web framework with macro capabilities. Here are a few examples of the
vastly different types of applications you can build in an instant:

##### ORM-backed CRUD application

`runserver.py`

```python

from whizbang.http.core import create_app
from whizbang.http.orm import create_engine
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

from whizbang.http.orm import Model, Column, String, DateTime, Integer, relationship, ForeignKey

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

###### View/edit object

![Single object shot](/images/resource.png)

##### NoSQL REST API application


