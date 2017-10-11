#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/9/29 上午9:51
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : model.py
# @Software: PyCharm
from .session import db
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, String, DateTime, Boolean

__author__ = 'blackmatrix'

BaseModel = declarative_base()


class ModelMixin:

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def upsert(self):
        db.add(self)
        return self

    def delete(self):
        db.delete(self)
        return self

    @property
    def columns(self):
        return (c.name for c in self.__table__.columns)

    @staticmethod
    def commit():
        db.commit()

    @classmethod
    def get_by_id(cls, id_):
        return db.query(cls).filter(cls.id == int(id_)).first()

    def to_dict(self, columns=None):
        """
        将SQLALCHEMY MODEL 转换成 dict
        :param columns: dict 的 key, 如果为None, 则返回全部列
        :return:
        """
        if columns is None:
            columns = self.columns
        return {c: getattr(self, c) for c in columns}


class ModelBase(BaseModel, ModelMixin):

    __abstract__ = True

    # 主键
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 创建人id
    creator_id = Column(Integer, nullable=True)
    # 创建人姓名
    creator_name = Column(String(30), nullable=True)
    # 创建时间
    create_time = Column(DateTime, nullable=True, default=datetime.now)
    # 最后更新时间
    # onupdate 表示任何列的更新都会触发重置此列
    update_time = Column(DateTime, nullable=True, onupdate=datetime.now)
    # 最后更新操作者id
    update_user_id = Column(Integer, nullable=True)
    # 最后更新操作者姓名
    update_user_name = Column(String(30), nullable=True)
    # 是否删除
    is_deleted = Column(Boolean, nullable=False, default=False)

    def __init__(self, *args, **kwargs):
        super(ModelBase, self).__init__(*args, **kwargs)

if __name__ == '__main__':
    pass
