"""Whizbang's ORM module."""
from sqlalchemy.ext.declarative import declarative_base


class Resource(object):
    __endpoint__ = None

    def to_json(self):
        values = {}
        for column in self.__table__.columns:
            values[column] = getattr(self, column)
        return values

    def __iter__(self):
        for column in self.__table__.columns:
            yield (column.name, getattr(self, column.name))

    @classmethod
    def endpoint(cls):
        return cls.__endpoint__ or '/' + cls.__tablename__

    def url(self):
        url = '/' + self.__endpoint__ + '/'
        url += getattr(self, self.__table__.primary_key.name)

Model = declarative_base(cls=(Resource,))
