#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/8/18 上午9:51
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : test_cache.py
# @Software: PyCharm
import unittest
from toolkit import Cache
from random import randint
from config import current_config

__author__ = 'blackmatrix'


cache = Cache(config=current_config)


class MemcachedTestCase(unittest.TestCase):

    def setUp(self):
        cache.delete_multi(('test_random', 'test_args', 'test_lru'))

    def tearDown(self):
        cache.delete_multi(('test_random', 'test_args', 'test_lru'))

    @staticmethod
    @cache.cached('test_random')
    def get_random():
        return randint(1, 999)

    @staticmethod
    @cache.cached('test_lru', maxsize=3)
    def add_random(a):
        return a + randint(1, 999)

    @staticmethod
    @cache.cached('test_args')
    def get_value(a, b, c, d, *args):
        return a, b, c, d, args

    def test_random_num(self):
        """
        通过生成随机数测试缓存时否生效
        :return:
        """
        num1 = self.get_random()
        num2 = self.get_random()
        num3 = self.get_random()
        assert num1 == num2 == num3

    def test_lru_cache(self):
        """
        通过添加随机数来测试lru cache
        :return:
        """
        num1 = self.add_random(1)
        num1_1 = self.add_random(1)
        num2 = self.add_random(2)
        num2_1 = self.add_random(2)
        # 缓存数量在maxsize之内，缓存不变
        assert num1 == num1_1
        assert num2 == num2_1
        # 参数为1的缓存被调用，优先级提高
        num1_2 = self.add_random(1)
        # 第三个缓存加入，缓存数量仍在maxsize之内，缓存不变
        # 开始清理优先级低的缓存，2 被清理
        num3 = self.add_random(3)
        num3_1 = self.add_random(3)
        assert num3 == num3_1
        # 缓存 1、2 仍保留，得到的值相等
        # 同时此操作会刷新缓存优先级
        num1_3 = self.add_random(1)
        num2_2 = self.add_random(2)
        assert num1 == num1_2 == num1_3
        assert num2 == num2_1 == num2_2
        # 缓存 4 加入，缓存总数超出maxsize
        num4 = self.add_random(4)
        num4_1 = self.add_random(4)
        assert num4 == num4_1
        # 缓存优先级最低的 3 被清理
        # 调用函数时，返回值变化
        num3_1 = self.add_random(3)
        assert num3 != num3_1
        # 缓存 5 加入，优先级最低的 1 被清理
        num5 = self.add_random(5)
        num5_1 = self.add_random(5)
        assert num5 == num5_1
        num1_4 = self.add_random(1)
        assert num1 != num1_4

    def test_arguments(self):
        """
        测试相同参数的多种传值方式
        :return:
        """
        result1 = self.get_value(1, 2, 3, 4)
        result2 = self.get_value(1, 2,  3, d=4)
        result3 = self.get_value(1, 2, c=3, d=4)
        result4 = self.get_value(1, 2, d=4, c=3)
        result5 = self.get_value(a=1, b=2, c=3, d=4)
        result6 = self.get_value(d=4, c=3, b=2, a=1)
        assert result1 == result2 == result3 == result4 == result5 == result6

if __name__ == '__main__':
    pass
