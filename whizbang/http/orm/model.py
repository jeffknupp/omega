"""Whizbang's ORM module."""
from sqlalchemy.ext.declarative import declarative_base


class Resource(object):
    def to_json(self):
        values = {}
        for column in self.__table__.columns:
            values[column] = getattr(self, column)
        return values

    def __iter__(self):
        for column in self.__table__.columns:
            yield (column.name, getattr(self, column.name))

Model = declarative_base(cls=(Resource,))
