#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/9/27 下午10:32
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: session
# @Software: PyCharm
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine as default_create_engine

__author__ = 'blackmatrix'


class Scope:

    def __init__(self):
        self._current_scope = None

    def set(self, value):
        self._current_scope = value

    def get(self):
        return self._current_scope


scope = Scope()


# 支持MySQL
def create_engine(config=None, connect_str=None, echo=True, max_overflow=10, encoding='utf-8'):
    config = config or {}
    echo = config.get('DB_ECHO', echo)
    encoding = config.get('DB_ENCODING', encoding)
    connect_str = config.get('DB_CONNECT', connect_str)
    max_overflow = config.get('DB_MAX_OVERFLOW', max_overflow)
    return default_create_engine(connect_str, echo=echo, max_overflow=max_overflow,
                                 encoding=encoding, pool_recycle=3600, pool_size=100)


# 支持SQLite
def create_sqlite_engine(config=None, connect_str=None, echo=True, encoding='utf-8'):
    config = config or {}
    echo = config.get('DB_ECHO', echo)
    encoding = config.get('DB_ENCODING', encoding)
    connect_str = config.get('DB_CONNECT', connect_str)
    return default_create_engine(connect_str, echo=echo, encoding=encoding, pool_recycle=3600)


databases = {}


def create_db(db_engine):
    return scoped_session(sessionmaker(autocommit=False, autoflush=True, expire_on_commit=False, bind=db_engine), scopefunc=scope.get)


def new_db(name, engine, db):
    databases.update({name: {'engine': engine, 'db': db}})


class DataBase:

    def __init__(self, config=None, connect_str=None, echo=True, max_overflow=5, encoding='utf-8'):
        self.config = config or {}
        self.echo = self.config.get('DB_ECHO', echo)
        self.encoding = self.config.get('DB_ENCODING', encoding)
        self.connect_str = self.config.get('DB_CONNECT', connect_str)
        self.max_overflow = self.config.get('DB_MAX_OVERFLOW', max_overflow)
        self._engine = None

    def create_engine(self):
        return create_engine(connect_str=self.connect_str, echo=self.echo, max_overflow=self.max_overflow, encoding=self.encoding)

    @property
    def engine(self):
        if self._engine is None:
            self._engine = self.create_engine()
        return self._engine

    @staticmethod
    def create_scoped_session(db_engine):
        return scoped_session(sessionmaker(autocommit=False, autoflush=True, expire_on_commit=False, bind=db_engine), scopefunc=scope.get)

    # 初始化数据库
    def init_db(self):
        from .model import Model
        Model.metadata.create_all(self.engine)

    # 销毁数据库
    def drop_db(self):
        from .model import Model
        Model.metadata.drop_all(self.engine)


class DataBaseSQLite(DataBase):

    def create_engine(self):
        return create_sqlite_engine(connect_str=self.connect_str, echo=self.echo, encoding=self.encoding)


if __name__ == '__main__':
    pass
