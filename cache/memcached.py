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


class CacheMeta(type):

    @staticmethod
    def key_prefix(func):
        @wraps(func)
        def _key_prefix(*args, **kwargs):
            return func(*args, **kwargs)
        return _key_prefix


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
                 socket_timeout=_SOCKET_TIMEOUT, cache_cas = False, flush_on_reconnect=0,
                 check_keys=True):
        if config:
            self.servers = config['CACHE_MEMCACHED_SERVERS']
            self.key_prefix = config['CACHE_KEY_PREFIX']
        else:
            self.servers = servers
            self.key_prefix = key_prefix
        super().__init__(servers=self.servers, debug=debug, pickleProtocol=pickleProtocol,
                         pickler=pickler, unpickler=unpickler, pload=pload, pid=pid,
                         server_max_key_length=server_max_key_length,
                         server_max_value_length=server_max_value_length, dead_retry=dead_retry,
                         socket_timeout=socket_timeout, cache_cas=cache_cas,
                         flush_on_reconnect=flush_on_reconnect, check_keys=check_keys)

    def get(self, key):
        new_key = '{0}_{1}'.format(self.key_prefix, key)
        return super().get(new_key)

    def set(self, key, val, time=0, min_compress_len=0):
        new_key = '{0}_{1}'.format(self.key_prefix, key)
        super().set(new_key, val, time, min_compress_len)

    def delete(self, key, time=0):
        new_key = '{0}_{1}'.format(self.key_prefix, key)
        super().delete(new_key, time)

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
    pass
