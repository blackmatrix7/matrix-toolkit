#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/8/18 下午2:00
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : test_config.py
# @Software: PyCharm
import unittest
from config import current_config

__author__ = 'blackmatrix'


class ConfigTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    def test_config_iter():
        keys = [key for key in current_config]
        assert isinstance(keys, list)

    @staticmethod
    def test_config_items():
        keys = {k: v for k, v in current_config.items()}
        assert isinstance(keys, dict)

    @staticmethod
    def test_get_value():
        value = current_config.get('TESTVALUE', 'TEST')
        assert value == 'TEST'

    @staticmethod
    def test_set_value():
        try:
            current_config.HELLO = 'ERROR'
        except Exception as ex:
            assert isinstance(ex, AttributeError)

    @staticmethod
    def test_get_item():
        assert current_config['DEBUG'] == False

if __name__ == '__main__':
    pass
