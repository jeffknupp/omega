"""Whizbang's ORM module."""
from sqlalchemy.ext.declarative import declarative_base


class Resource(object):
    def to_json(self):
        values = {}
        for column in self.__table__.columns:
            values[column] = getattr(self, column)
        return values


Model = declarative_base(cls=(Resource,))
