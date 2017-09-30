#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/9/27 下午10:32
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: session.py
# @Software: PyCharm

from config import current_config
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
        self.config = config or {}
        self.echo = self.config.get('DB_ECHO', echo)
        self.encoding = self.config.get('DB_ENCODING', encoding)
        self.connect_str = self.config.get('DB_CONNECT', connect_str)
        self.max_overflow = self.config.get('DB_MAX_OVERFLOW', max_overflow)
        self._engine = None

    def create_engine(self):
        return create_engine(self.connect_str, echo=self.echo, max_overflow=self.max_overflow, encoding=self.encoding)

    @property
    def engine(self):
        if self._engine is None:
            self._engine = self.create_engine()
        return self._engine


def create_db(engin):
    return scoped_session(sessionmaker(autocommit=False, autoflush=True, expire_on_commit=False, bind=engine), scopefunc=scope.get)

engine = DataBase(connect_str=current_config.WORKFLOW_DB_CONNECT).engine

db = create_db(engine)


if __name__ == '__main__':
    pass
