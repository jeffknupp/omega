import datetime

from whizbang.http.orm import (
    Model,
    Column,
    String,
    DateTime,
    Integer,
    relationship,
    ForeignKey,
    )


class User(Model):
    """A Twooter User"""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    joined_at = Column(DateTime, default=datetime.datetime.now())


class Twoot(Model):
    """A Twoot message"""
    __tablename__ = 'twoot'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    posted_at = Column(DateTime, default=datetime.datetime.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
