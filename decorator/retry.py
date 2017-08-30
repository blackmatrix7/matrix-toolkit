#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/8/24 20:36
# @Author  : BlackMatrix
# @Site : 
# @File : retry.py
# @Software: PyCharm
from time import sleep
from functools import wraps

__author__ = 'blackmatrix'


"""
在函数执行出现异常时自动重试的简单装饰器
"""


def retry(max_retries: int =5, delay: int =0, step: int =0, exceptions: tuple =(Exception,), sleep_func=sleep):
    """
    函数执行出现异常时自动重试的简单装饰器
    :param max_retries:  最多重试次数
    :param delay:  每次重试的延迟，单位秒
    :param step:  每次重试后延迟递增，单位秒
    :param exceptions:  触发重试的异常类型
    :param sleep_func:  实现延迟的方法，默认为time.sleep，在一些异步框架，如
    tornado中，使用time.sleep会导致阻塞，可以传入自定义的方法来实现延迟。
    自定义方法函数签名应类似time.sleep，接收一个参数，为延迟执行的时间。
    :return: 
    """
    def wrapper(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            nonlocal delay, step, max_retries, exceptions
            func_ex = None
            while max_retries > 0:
                try:
                    return func(*args, **kwargs)
                except exceptions as ex:
                    func_ex = ex
                finally:
                    max_retries -= 1
                    if delay > 0 or step > 0:
                        sleep_func(delay)
                        delay += step
            else:
                raise func_ex
        return _wrapper
    return wrapper


if __name__ == '__main__':
    pass
