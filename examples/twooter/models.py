import datetime
import uuid

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

    uuid = Column(String, primary_key=True)
    content = Column(String)
    posted_at = Column(DateTime, default=datetime.datetime.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
