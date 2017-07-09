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
from inspect import signature, Parameter
__author__ = 'blackmatrix'

SERVER_MAX_KEY_LENGTH = 250
SERVER_MAX_VALUE_LENGTH = 1024*1024
_DEAD_RETRY = 30
_SOCKET_TIMEOUT = 3


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

        super().__init__(servers=self.servers, debug=debug, pickleProtocol=pickleProtocol,
                         pickler=pickler, unpickler=unpickler, pload=pload, pid=pid,
                         server_max_key_length=server_max_key_length,
                         server_max_value_length=server_max_value_length, dead_retry=dead_retry,
                         socket_timeout=socket_timeout, cache_cas=cache_cas,
                         flush_on_reconnect=flush_on_reconnect, check_keys=check_keys)

    def get(self, key):
        key = '{0}_{1}'.format(self.key_prefix, key)
        return super().get(key)

    def set(self, key, val, time=0, min_compress_len=0):
        key = '{0}_{1}'.format(self.key_prefix, key)
        super().set(key, val, time, min_compress_len)

    def delete(self, key, time=0):
        key = '{0}_{1}'.format(self.key_prefix, key)
        super().delete(key, time)

    def incr(self, key, delta=1):
        key = '{0}_{1}'.format(self.key_prefix, key)
        return super().incr(key=key, delta=delta)

    def decr(self, key, delta=1):
        key = '{0}_{1}'.format(self.key_prefix, key)
        return super().decr(key=key, delta=delta)

    def add(self, key, val, time=0, min_compress_len=0):
        key = '{0}_{1}'.format(self.key_prefix, key)
        return super().add(key=key, val=val, time=time, min_compress_len=min_compress_len)

    def append(self, key, val, time=0, min_compress_len=0):
        key = '{0}_{1}'.format(self.key_prefix, key)
        return super().append(key=key, val=val, time=time, min_compress_len=min_compress_len)

    def prepend(self, key, val, time=0, min_compress_len=0):
        key = '{0}_{1}'.format(self.key_prefix, key)
        return super().prepend(key=key, val=val, time=time, min_compress_len=min_compress_len)

    def replace(self, key, val, time=0, min_compress_len=0):
        key = '{0}_{1}'.format(self.key_prefix, key)
        return super().replace(key=key, val=val, time=time, min_compress_len=min_compress_len)

    def cas(self, key, val, time=0, min_compress_len=0):
        key = '{0}_{1}'.format(self.key_prefix, key)
        return super().cas(key=key, val=val, time=time, min_compress_len=min_compress_len)

    def set_multi(self, mapping, time=0, key_prefix='', min_compress_len=0):
        # TODO 团队太穷，只有一台memcached服务器，所以这种情况无法测试验证是否正常，留着以后有机会再完成
        return super().set_multi(mapping=mapping, time=time, key_prefix=key_prefix, min_compress_len=min_compress_len)

    def gets(self, key):
        key = '{0}_{1}'.format(self.key_prefix, key)
        return super().gets(key)

    def get_multi(self, keys, key_prefix=''):
        # TODO 团队太穷，只有一台memcached服务器，所以这种情况无法测试验证是否正常，留着以后有机会再完成
        keys = ['{0}_{1}'.format(self.key_prefix, key) for key in keys]
        return super().get_multi(keys, key_prefix=key_prefix)

    def check_key(self, key, key_extra_len=0):
        key = '{0}_{1}'.format(self.key_prefix, key)
        return super().check_key(key=key, key_extra_len=key_extra_len)

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

    print('初始化缓存客户端')

    cache = Cache(servers=['127.0.0.1:11211'], key_prefix='hello')

    @cache.cached('test_cache')
    def get_random():
        return randint(1, 8)

    print('读取缓存')

    print(get_random())

    print('删除缓存')

    cache.delete('test_cache')

    print('重新设置缓存')

    print(get_random())
