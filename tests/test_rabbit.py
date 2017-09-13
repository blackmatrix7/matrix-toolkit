#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/9/8 下午4:20
# @Author : BlackMatrix
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
        messages = '[{"user": "jim", "age: 1,3,}, {"user": "jack", "age": 24}]'
        result = self.send_messages(messages=messages)
        assert result == {'success': 1, 'message': 1, 'error': [], 'failed': 0}
        self.rabbitmq.disconnect()

    def test_close_and_open(self):
        """
        测试连接rabbitmq和断开连接
        :return:
        """
        self.rabbitmq.connect()
        assert not self.rabbitmq.connection.is_closed
        self.rabbitmq.connect()
        assert not self.rabbitmq.connection.is_closed
        self.rabbitmq.connect()
        assert not self.rabbitmq.connection.is_closed
        self.rabbitmq.disconnect()
        assert not self.rabbitmq.connection.is_closed
        self.rabbitmq.disconnect()
        assert not self.rabbitmq.connection.is_closed
        self.rabbitmq.disconnect()
        assert self.rabbitmq.connection.is_closed
        self.rabbitmq.disconnect()

    def test_context(self):
        """
        测试以上下文的形式管理rabbitmq连接
        :return:
        """
        with self.rabbitmq as rabbit:
            # 自动打开连接
            assert not rabbit.connection.is_closed
            result = rabbit.send_message(exchange_name='test_exchange',
                                         queue_name='test_queue',
                                         messages=[1, 2, 3])
            assert result == {'success': 3, 'message': 3, 'error': [], 'failed': 0}
        # 上下文执行完成后，自动关闭连接
        assert self.rabbitmq.connection.is_closed

    def test_send_msg_decorator(self):
        """
        测试以装饰器的形式，将被装饰函数的执行结果发送到rabbitmq
        :return:
        """
        @self.rabbitmq.send_to_rabbitmq(exchange_name='test_exchange', queue_name='test_queue')
        def send_msg():
            return [1, 2, 3, 4]
        result = send_msg()
        assert result == [1, 2, 3, 4]

    def test_receive_msg_decorator(self):
        pass


if __name__ == '__main__':
    pass
