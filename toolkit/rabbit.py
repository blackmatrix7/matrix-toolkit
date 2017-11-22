#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/9/8 下午3:38
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : rabbitmq.py
# @Software: PyCharm
import pika
import json
from functools import wraps
from json.decoder import JSONDecodeError

__author__ = 'blackmatrix'

"""
一个支持上下文的rabbitmq操作对象
"""


class RabbitMQ:

    def __init__(self, user: str=None, pwd: str=None, host: str=None, port: int=5672, config: dict=None):
        self.config = config or {}
        self.user = user or config.get('RABBITMQ_USER')
        self.pwd = pwd or config.get('RABBITMQ_PASS')
        self.host = host or config.get('RABBITMQ_HOST')
        self.port = port or config.get('RABBITMQ_PORT')
        self.connection = None
        self.channel = None
        # 计算上下文管理器连接的次数
        self.connect_count = 0

    def connect(self):
        """
        当rabbitmq 未连接时，自动连接，如果已连接，不进行任何操作
        :return:
        """
        if self.connect_count <= 0 and self.connection is None or self.connection.is_closed:
            credentials = pika.PlainCredentials(self.user, self.pwd)
            parameters = pika.ConnectionParameters(self.host, self.port, '/', credentials)
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
        self.connect_count += 1

    def disconnect(self):
        """
        当连接打开时，断开连接
        :return:
        """
        self.connect_count -= 1
        if self.connect_count <= 0 and self.connection.is_open:
            self.channel.close()
            self.connection.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    # 用于发送消息到指定的交换机，并绑定队列到对应的交换机
    def send_message(self, exchange_name, queue_name, messages, exchange_type='direct',
                     passive=False, durable=True, auto_delete=False, internal=False):
        """
        向RabbitMQ发送消息，需手动连接rabbitmq，消息发送完成后，需手动断开连接
        :param exchange_name: 交换机名称
        :param queue_name: 队列名称
        :param messages: 消息内容，单条消息可以str、dict传入，多条消息以list、tuple或其它可迭代对象传入
        :param exchange_type: 交换机类型，包括 fanout, direct 和 topic。
        :param passive: true if we are passively declaring a exchange (asserting the exchange already exists)
        :param durable: 持久化
        :param auto_delete: 当所有绑定队列都不再使用时，是否自动删除该交换机
        :param internal:
        :return:
        """
        # 声明交换机
        self.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type,
                                      passive=passive, durable=durable, auto_delete=auto_delete,
                                      internal=internal)
        # 声明队列
        self.channel.queue_declare(queue=queue_name, durable=True)
        # 将队列绑定到交换机上，并设置路由键，将队列名称和路由键设置一致便于理解和管理
        self.channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=queue_name)
        # JSON格式支持
        try:
            messages = json.loads(messages)
        except (TypeError, JSONDecodeError):
            pass
        # 判断消息类型
        try:
            iter(messages)
            # 对于dict和str不进行迭代
            if isinstance(messages, (str, dict)):
                raise TypeError
            items = messages
        except (TypeError, ValueError):
            items = [messages]
        # 尝试发送到消息队列的数量
        message_count = 0
        # 成功的数量
        success_count = 0
        # 失败的数量
        failed_count = 0
        # 异常信息
        error_list = []
        for message in items:
            message_count += 1
            # 异常捕获，在出现异常时保证循环继续
            try:
                # 无法转换为json的，直接发送
                try:
                    message = json.dumps(message, ensure_ascii=False)
                except ValueError:
                    pass
                # 发送消息到指定的队列，交换机为了识别方便，指定名称，不使用匿名交换机，delivery_mode为2表示消息持久化
                self.channel.basic_publish(exchange=exchange_name, routing_key=queue_name, body=message,
                                           properties=pika.BasicProperties(delivery_mode=2))
                success_count += 1
            except BaseException as ex:
                error_list.append({'message': message, 'error': ex})
                failed_count += 1
        retinfo = {'message': message_count, 'success': success_count, 'failed': failed_count, 'error': error_list}
        return retinfo

    # 使用此装饰器将被装饰的函数的返回结果发送消息到RabbitMQ
    def send_to_rabbitmq(self, exchange_name, queue_name, exchange_type='direct', passive=False,
                         durable=True, auto_delete=False, internal=False):
        """
        装饰器，可将被装饰的函数的返回值发送到消息队列，不推荐使用，建议使用send_message直接发送。
        :param exchange_name:
        :param queue_name:
        :param exchange_type:
        :param passive:
        :param durable:
        :param auto_delete:
        :param internal:
        :return:
        """
        def _send_to_rabbitmq(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                messages = func(*args, **kwargs)
                self.connect()
                self.send_message(exchange_name=exchange_name, queue_name=queue_name, messages=messages,
                                  exchange_type=exchange_type, passive=passive, durable=durable,
                                  auto_delete=auto_delete, internal=internal)
                self.disconnect()
                return messages
            return wrapper
        return _send_to_rabbitmq

    # 使用此装饰器，从RabbitMQ消费消息
    def receive_from_rabbitmq(self, exchange_name, queue_name, routing_key, exchange_type='direct',
                              passive=False, durable=True, auto_delete=False, internal=False):
        def _receive_from_rabbitmq(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # 回调函数，用于消费消息及消息确认
                def callback(ch, method, properties, body):
                    # 获取消费消息的结果，True或者False
                    result = func(*args, message=body, **kwargs)
                    if result is True:
                        # 返回结果为True时，进行消息确认，此时RabbitMQ才从消息队列中移除消息
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                    else:
                        # 返回结果为False时，不进行消息确认，将消息重新加入消息队列，等待下次处理
                        ch.basic_nack(delivery_tag=method.delivery_tag)
                self.connect()
                # 声明交换机
                self.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type,
                                              passive=passive, durable=durable, auto_delete=auto_delete,
                                              internal=internal)
                # 声明队列
                self.channel.queue_declare(queue=queue_name, durable=True)
                # 将队列绑定到交换机上，并设置路由键
                self.channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)
                # 关闭自动应答，在执行callback后再进行消息确认，此时rabbitmq才会移除此消息
                self.channel.basic_consume(callback, queue=queue_name, no_ack=False)
                # 开始接收消息
                self.channel.start_consuming()
            return wrapper
        return _receive_from_rabbitmq


if __name__ == '__main__':
    pass
