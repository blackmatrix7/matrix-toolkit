#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/7/9 下午1:28
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: cache
# @Software: PyCharm
import pickle
from memcache import Client
from functools import wraps

__author__ = 'blackmatrix'

SERVER_MAX_KEY_LENGTH = 250
SERVER_MAX_VALUE_LENGTH = 1024*1024
_DEAD_RETRY = 30
_SOCKET_TIMEOUT = 3


def set_key_prefix(key_prefix=''):

    def _set_key_prefix(func):
        """
        如果类中的函数或方法存在key关键字，就给key的值加上一个前缀
        :param func:
        :return:
        """
        @wraps(func)
        def _key_prefix(*args, **kwargs):
            print('装饰器已应用')
            return func(*args, **kwargs)
        return _key_prefix

    return _set_key_prefix


class CacheMeta(type):

    def __new__(mcs,  clsname, supers, clsdict):
        return super().__new__(mcs, clsname, supers, clsdict)

    def __init__(cls, clsname, supers, clsdict):
        for attr in dir(cls):
            value = getattr(cls, attr)
            if callable(value) and not attr.startswith('_'):
                setattr(cls, attr, set_key_prefix()(value))
        super().__init__(clsname, supers, clsdict)


class Cache(Client):

    """
    一个基于Python3-Memcached的简单缓存操作类
    主要解决的是当不同的环境使用同一memcached服务器时，
    带来的数据竞态问题。
    """

    def __init__(self, *, config=None, servers: list = None, key_prefix: str='',
                 debug=0, pickleProtocol=0, pickler=pickle.Pickler, unpickler=pickle.Unpickler,
                 pload=None, pid=None, server_max_key_length=SERVER_MAX_KEY_LENGTH,
                 server_max_value_length=SERVER_MAX_VALUE_LENGTH, dead_retry=_DEAD_RETRY,
                 socket_timeout=_SOCKET_TIMEOUT, cache_cas=False, flush_on_reconnect=0,
                 check_keys=True):
        if config:
            self.servers = config['CACHE_MEMCACHED_SERVERS']
            self.key_prefix = config['CACHE_KEY_PREFIX']
        else:
            self.servers = servers
            self.key_prefix = key_prefix

        for attr in dir(self):
            value = getattr(self, attr)
            if callable(value) and not attr.startswith('_'):
                setattr(self, attr, set_key_prefix()(value))
        super().__init__(servers=self.servers, debug=debug, pickleProtocol=pickleProtocol,
                         pickler=pickler, unpickler=unpickler, pload=pload, pid=pid,
                         server_max_key_length=server_max_key_length,
                         server_max_value_length=server_max_value_length, dead_retry=dead_retry,
                         socket_timeout=socket_timeout, cache_cas=cache_cas,
                         flush_on_reconnect=flush_on_reconnect, check_keys=check_keys)

    def cached(self, key, time_seconds=36000):
        """
        函数装饰器，装饰到无参数的函数上时，会优先返回缓存的值
        :param key:
        :param time_seconds:
        :return:
        """
        def _cached(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                args_cache = self.get(key)
                if args_cache:
                    return args_cache
                else:
                    result = func(*args, **kwargs)
                    self.set(key=key, val=result, time=time_seconds)
                    return result
            return wrapper
        return _cached

    def delcache(self, key):
        """
        清理缓存装饰器，装饰到函数上时，每次函数执行完毕会清理对应的缓存
        :param key:
        :return:
        """
        def _delcache(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                self.delete(key)
                return result
            return wrapper
        return _delcache


if __name__ == '__main__':
    from random import randint

    cache = Cache(servers=[])

    @cache.cached('test_cache')
    def get_random():
        return randint(1, 8)

    print(get_random())

    cache.delete('test_cache')

    print(get_random())
