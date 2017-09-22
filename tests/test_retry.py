#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/8/24 21:01
# @Author  : BlackMatrix
# @Site : 
# @File : test_retry.py
# @Software: PyCharm
import unittest
from toolkit import retry
from random import randint
from toolkit.retry import StopRetry
__author__ = 'blackmatrix'

"""
测试retry装饰器是否正常工作
"""

count = 0


def callback(ex):
    assert isinstance(ex, BaseException)


def callback2(ex):
    global count
    count += 1
    return True


def callback3(ex):
    global count
    count += 1
    raise RuntimeError


def validate1(result):
    global count
    count += 1
    return False


class RetryTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    @retry(max_retries=30, delay=1, step=1, exceptions=RuntimeError)
    def func_for_retry():
        """
        测试重试的函数，利用随机数，有一定概率抛出RuntimeError
        :return: 
        """
        i = randint(1, 5)
        print(i)
        if i != 1:
            raise RuntimeError
        else:
            return 'python'

    @staticmethod
    @retry(max_retries=30, delay=0, step=0, exceptions=RuntimeError)
    def func_for_retry2():
        """
        测试重试的函数，利用随机数，有一定概率抛出KeyError
        测试引发的异常类型与重试装饰器的异常类型不同时，能否正常抛出异常
        :return:
        """
        i = randint(1, 5)
        if i != 1:
            raise KeyError
        else:
            return 'python'

    @staticmethod
    @retry(max_retries=30, delay=0, step=0, exceptions=(RuntimeError, KeyError))
    def func_for_retry3():
        """
        测试重试的函数，利用随机数，有一定概率抛出KeyError
        测试传入多个异常类型是否能正常工作
        :return:
        """
        i = randint(1, 5)
        if i != 1:
            raise KeyError
        else:
            return 'python'

    @staticmethod
    @retry(max_retries=30, delay=0, step=0, exceptions=KeyError, callback=callback)
    def func_for_retry4():
        """
        测试重试的函数，利用随机数，有一定概率抛出KeyError
        测试回调函数是否正常工作
        :return:
        """
        i = randint(1, 5)
        if i != 1:
            raise KeyError
        else:
            return 'python'

    @staticmethod
    @retry(max_retries=30, delay=0, step=0, exceptions=KeyError, callback=callback2)
    def func_for_retry5():
        """
        测试回调函数返回True时，终止重试
        :return:
        """
        raise KeyError

    @staticmethod
    @retry(max_retries=30, delay=0, step=0, exceptions=KeyError, callback=callback3)
    def func_for_retry6():
        """
        测试回调函数抛出异常时，终止重试
        :return:
        """
        pass

    @staticmethod
    @retry(max_retries=5, delay=0, step=0, exceptions=KeyError,  validate=validate1)
    def func_for_retry7():
        """
        测试当验证函数返回False时，即使函数不出错也继续重试
        :return:
        """
        print('func_for_retry7')

    @staticmethod
    @retry(max_retries=5, delay=0, step=0, exceptions=KeyError,  validate=validate1)
    def func_for_retry7():
        """
        测试当验证函数返回False时，即使函数不出错也继续重试
        :return:
        """
        print('func_for_retry7')

    def test_func_retry(self):
        """
        测试有一定概率抛出异常，能正常重试并返回结果
        :return:
        """
        global count
        assert callable(callback)
        assert self.func_for_retry() == 'python'

    def test_func_retry2(self):
        """
        测试引发的异常类型与重试装饰器的异常类型不同时，能否正常抛出异常
        :return:
        """
        try:
            self.func_for_retry2()
        except Exception as ex:
            assert isinstance(ex, KeyError)

    def test_func_retry3(self):
        """
        测试传入多个异常类型是否能正常工作
        :return:
        """
        self.func_for_retry3()

    def test_func_retry4(self):
        """
        测试回调函数是否正常工作
        :return:
        """
        self.func_for_retry4()

    def test_func_retry5(self):
        """
        测试回调函数返回True时，终止重试
        :return:
        """
        self.func_for_retry5()

    def test_func_retry6(self):
        """
        测试回调函数抛出异常时，终止重试
        :return:
        """
        global count
        try:
            self.func_for_retry6()
        except Exception as ex:
            assert isinstance(ex, StopRetry)
        finally:
            assert count <= 1
            count = 0

    def test_func_retry7(self):
        """
        测试当验证函数返回False时，即使函数不出错也继续重试
        :return:
        """
        global count
        try:
            self.func_for_retry7()
        except Exception as ex:
            assert isinstance(ex, StopRetry)
        finally:
            assert count == 5
            count = 0

if __name__ == '__main__':
    pass
