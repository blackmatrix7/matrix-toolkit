#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/9/27 下午10:32
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: session
# @Software: PyCharm
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

__author__ = 'blackmatrix'


class Scope:

    def __init__(self):
        self._current_scope = None

    def set(self, value):
        self._current_scope = value

    def get(self):
        return self._current_scope


scope = Scope()


class DataBase:

    def __init__(self, config=None, connect_str=None, echo=True, max_overflow=5, encoding='utf-8'):
        config = config or {}
        self.echo = config.get('DB_ECHO', echo)
        self.encoding = config.get('DB_ENCODING', encoding)
        self.connect_str = config.get('DB_CONNECT', connect_str)
        self.max_overflow = config.get('DB_MAX_OVERFLOW', max_overflow)
        self.engine = None

    def create_engine(self):
        if self.engine is None:
            self.engine = create_engine(self.connect_str, echo=self.echo, max_overflow=self.max_overflow, encoding=self.encoding)
        return self.engine

    @property
    def scoped_session(self):
        session = scoped_session(sessionmaker(autocommit=False, autoflush=True, expire_on_commit=False, bind=engine, scopefunc=scope.get))
        return session


if __name__ == '__main__':
    pass
