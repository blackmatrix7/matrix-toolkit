#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/8/24 21:01
# @Author  : BlackMatrix
# @Site : 
# @File : test_retry.py
# @Software: PyCharm
import unittest
from random import randint
from decorator.retry import retry
__author__ = 'blackmatrix'

"""
测试retry装饰器是否正常工作
"""


class RetryTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    @retry(max_retries=30, delay=0, step=0, exceptions=(TypeError,))
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

    def test_retry(self):
        assert self.func_for_retry() == 'python'

if __name__ == '__main__':
    pass
