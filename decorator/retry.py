#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/8/24 20:36
# @Author  : BlackMatrix
# @Site : 
# @File : retry.py
# @Software: PyCharm
from functools import wraps

__author__ = 'blackmatrix'


"""
一个在函数执行出现异常时自动重试的简单装饰器
不支持每次重试的间隔是因为如果简单的用time.sleep会导致一些异步的web框架阻塞
比如tornado
"""


def retry(max_retries=5):
    """
    函数执行出现异常时自动重试的简单装饰器
    :param max_retries:  最多重试次数
    :return: 
    """
    def wrapper(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            nonlocal max_retries
            func_ex = None
            while max_retries > 0:
                try:
                    return func(*args, **kwargs)
                except Exception as ex:
                    func_ex = ex
                    max_retries -= 1
            else:
                raise func_ex
        return _wrapper
    return wrapper


if __name__ == '__main__':
    pass
