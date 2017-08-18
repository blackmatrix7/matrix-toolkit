#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/7/9 下午1:28
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: cache
# @Software: PyCharm
import pickle
import hashlib
import unittest
from memcache import Client
from functools import wraps
from inspect import signature
from config import current_config
from collections import deque, OrderedDict

__author__ = 'blackmatrix'

SERVER_MAX_KEY_LENGTH = 250
SERVER_MAX_VALUE_LENGTH = 1024*1024
_DEAD_RETRY = 30
_SOCKET_TIMEOUT = 3
_NO_VALUE = object()


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
            self.debug = config['DEBUG']
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
        key = '{0}{1}'.format(self.key_prefix, key)
        return super().get(key)

    def set(self, key, val, time=0, min_compress_len=0):
        key = '{0}{1}'.format(self.key_prefix, key)
        super().set(key, val, time, min_compress_len)

    def delete(self, key, time=0):
        key = '{0}{1}'.format(self.key_prefix, key)
        super().delete(key, time)

    def incr(self, key, delta=1):
        key = '{0}{1}'.format(self.key_prefix, key)
        return super().incr(key=key, delta=delta)

    def decr(self, key, delta=1):
        key = '{0}{1}'.format(self.key_prefix, key)
        return super().decr(key=key, delta=delta)

    def add(self, key, val, time=0, min_compress_len=0):
        key = '{0}{1}'.format(self.key_prefix, key)
        return super().add(key=key, val=val, time=time, min_compress_len=min_compress_len)

    def append(self, key, val, time=0, min_compress_len=0):
        key = '{0}{1}'.format(self.key_prefix, key)
        return super().append(key=key, val=val, time=time, min_compress_len=min_compress_len)

    def prepend(self, key, val, time=0, min_compress_len=0):
        key = '{0}{1}'.format(self.key_prefix, key)
        return super().prepend(key=key, val=val, time=time, min_compress_len=min_compress_len)

    def replace(self, key, val, time=0, min_compress_len=0):
        key = '{0}{1}'.format(self.key_prefix, key)
        return super().replace(key=key, val=val, time=time, min_compress_len=min_compress_len)

    def cas(self, key, val, time=0, min_compress_len=0):
        key = '{0}{1}'.format(self.key_prefix, key)
        return super().cas(key=key, val=val, time=time, min_compress_len=min_compress_len)

    def set_multi(self, mapping, time=0, key_prefix='', min_compress_len=0):
        return super().set_multi(mapping=mapping, time=time, key_prefix=key_prefix, min_compress_len=min_compress_len)

    def gets(self, key):
        key = '{0}{1}'.format(self.key_prefix, key)
        return super().gets(key)

    def get_multi(self, keys, key_prefix=''):
        keys = ['{0}{1}'.format(self.key_prefix, key) for key in keys]
        return super().get_multi(keys, key_prefix=key_prefix)

    def check_key(self, key, key_extra_len=0):
        key = '{0}{1}'.format(self.key_prefix, key)
        return super().check_key(key=key, key_extra_len=key_extra_len)

    @staticmethod
    def _create_args_sig(func, params,  *args,  **kwargs):
        # 函数名称
        func_name = func.__name__ if callable(func) else func
        args_count = len(args)
        # 复制一份函数参数列表，避免对外部数据的修改
        args = list(args)
        # 将 POSITIONAL_OR_KEYWORD 的参数转换成 k/w 的形式
        if args:
            for index, (key, value) in enumerate(params.items()):
                if str(value.kind) == 'POSITIONAL_OR_KEYWORD':
                    if index < args_count:
                        kwargs.update({key: args.pop(0)})
        # 对参数进行排序
        args.extend(({k: kwargs[k]} for k in sorted(kwargs.keys())))
        func_args = '{0}{1}'.format(func_name, pickle.dumps(args))
        args_sig = hashlib.sha256(func_args.encode()).hexdigest()
        return args_sig

    def cached(self, key, timeout=36000, maxsize=20):
        """
        函数装饰器，装饰到函数上时，会优先返回缓存的值
        :param key:
        :param timeout:
        :param maxsize:
        :return:
        """
        def _cached(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # 获取函数参数
                func_params = signature(func).parameters
                # 获取函数参数并创建签名
                args_sig = self._create_args_sig(func, func_params, *args, **kwargs)
                # 从缓存里获取数据
                func_cache = self.get(key) or OrderedDict()
                # 通过函数签名判断函数是否被进行过修改, 如果进行过修改，不能读取缓存的数据
                result = func_cache.get(args_sig, _NO_VALUE)
                # 超出限制大小则删除最早的缓存，统计大小时需要排除lru这个key
                if len(func_cache) >= maxsize and args_sig not in func_cache:
                    func_cache.popitem(last=False)
                if args_sig in func_cache:
                    func_cache.move_to_end(args_sig)
                if result == _NO_VALUE:
                    result = func(*args, **kwargs)
                    # 保存函数执行结果
                    func_cache.update({args_sig: result})
                self.set(key=key, val=func_cache, time=timeout)
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
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as ex:
                    raise ex
                finally:
                    self.delete(key)
            return wrapper
        return _delcache


if __name__ == '__main__':
    pass



