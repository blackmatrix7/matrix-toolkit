#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/9/8 下午4:20
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : test_rabbitmq.py
# @Software: PyCharm
import unittest
from tookit import RabbitMQ
from functools import partial
from config import current_config

__author__ = 'blackmatrix'


class RabbitTestCase(unittest.TestCase):

    def setUp(self):
        self.rabbitmq = RabbitMQ(config=current_config)
        self.send_messages = partial(self.rabbitmq.send_message,
                                     exchange_name='test_exchange',
                                     queue_name='test_queue')

    def tearDown(self):
        pass

    def test_send_msg_list(self):
        self.rabbitmq.connect()
        messages = [1, 2, 3, 4, 5, 6]
        result = self.send_messages(messages=messages)
        assert result == {'failed': 0, 'message': 6, 'success': 6, 'error': []}
        self.rabbitmq.disconnect()

    def test_send_msg_dict(self):
        self.rabbitmq.connect()
        messages = {'name': 'jim', 'age': 13}
        result = self.send_messages(messages=messages)
        assert result == {'success': 1, 'message': 1, 'error': [], 'failed': 0}
        self.rabbitmq.disconnect()

    def test_send_msg_json(self):
        """
        测试json字符串
        :return:
        """
        self.rabbitmq.connect()
        messages = '{"user": "jim", "age": 13}'
        result = self.send_messages(messages=messages)
        assert result == {'success': 1, 'message': 1, 'error': [], 'failed': 0}
        self.rabbitmq.disconnect()

    def test_send_msg_json2(self):
        """
        测试json字符串
        :return:
        """
        self.rabbitmq.connect()
        messages = '[{"user": "jim", "age": 13}, {"user": "jack", "age": 24}]'
        result = self.send_messages(messages=messages)
        assert result == {'success': 2, 'message': 2, 'error': [], 'failed': 0}
        self.rabbitmq.disconnect()

    def test_send_msg_json3(self):
        """
        测试错误的json字符串，如果需要发送json到消息队列，需要将json存放在list中
        :return:
        """
        self.rabbitmq.connect()
        messages = ['[{"user": "jim", "age": 13}, {"user": "jack", "age": 24}]']
        result = self.send_messages(messages=messages)
        assert result == {'success': 1, 'message': 1, 'error': [], 'failed': 0}
        self.rabbitmq.disconnect()

    def test_send_msg_err_json(self):
        """
        测试错误的json字符串,错误的json字符串会被当成普通字符串处理
        :return:
        """
        self.rabbitmq.connect()
        messages = '[{"user": "jim", "age: 13}, {"user": "jack", "age": 24}]'
        result = self.send_messages(messages=messages)
        assert result == {'success': 1, 'message': 1, 'error': [], 'failed': 0}
        self.rabbitmq.disconnect()

if __name__ == '__main__':
    pass
