#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/7/15 上午12:15
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: huawei
# @Software: PyCharm
import json
import calendar
from datetime import datetime
from cache.cache import Cache
from json import JSONDecodeError
from abc import ABCMeta, abstractmethod
from dateutil.relativedelta import relativedelta

__author__ = 'blackmatrix'


"""
轻量化的华为推送客户端
"""

# 模拟一个缓存服务器，可以使用Flask-Caching，也可以使用cache/cache.py下的缓存模块
cache = Cache(servers=['127.0.0.1:11211'])


class IPush(metaclass=ABCMeta):

    @abstractmethod
    def push(self, targets, title, content, settings):
        pass


class HuaWeiPush(IPush):

    # 读取连接配置
    def __init__(self, app_id, app_secret, ver='1',
                 token_url='https://login.vmall.com/oauth2/token',
                 push_url='https://api.push.hicloud.com/pushsend.do'):
        self.ver = ver
        self.app_id = app_id
        self.app_secret = app_secret
        self.token_url = token_url
        self.push_url = push_url

    # 请求 token
    @property
    @cache.cached(time_seconds=432000, key='hw_token')
    def token(self):
        """
        获取华为推送的token，并利用缓存机制管理token。
        缓存的有效期需要设置得比token的有效期短，当无法从缓存读取token时，
        则执行函数，获取新的token，并且重新进行缓存。
        :return:
        """
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        resp = WebRequests.requests(method='post', headers=headers,
                                    url=self.token_url,
                                    data={'grant_type': 'client_credentials',
                                          'client_id': self.app_id,
                                          'client_secret': self.app_secret})
        print(resp)
        return resp.get('access_token') if resp else None

    @token.deleter
    @cache.delcache(key='hw_token')
    def token(self):
        pass

    # 消息推送
    def push(self, targets, title, content, settings=None):
        """
        华为推送消息实现
        :param targets: 推送的目标设备 token
        :param title: 推送的标题
        :param content: 推送的内容
        :param settings: 其他推送设置，dict或json格式字符串
        :return:
        """
        if settings is None:
            settings = {'type': 3,
                        'action': {'type': 3, 'param': {'appPkgName': 'com.example.jg'}},
                        'ext': {'biTag': 'vcan'}}
        elif 'type' in settings and 'ext' in settings:
            # 透传消息，不需要 action
            if settings['type'] == 1:
                settings = dict(settings)
            # 通知栏异步消息，需要检验json完整性
            elif settings['type'] == 3 \
                    and 'action' in settings \
                    and 'type' in settings['action'] \
                    and 'param' in settings['action']:
                settings = dict(settings)
            else:
                raise JSONDecodeError
        else:
            raise JSONDecodeError

        # 推送消息主体
        if settings['type'] == 1:
            payload = {
                'hps': {
                    'msg': {
                        'type': 1,
                        'body': content
                    }
                }
            }
        elif settings['type'] == 3:
            payload = {
                'hps': {
                    'msg': {
                        'type': 3,
                        'body': {
                            'content': content,
                            'title': title
                        },
                        'action': settings['action']
                        }
                    },
                'ext': settings['ext']
            }
        else:
            raise JSONDecodeError

        resp = self.push_raw_json(payload, targets)
        return resp

    def push_raw_json(self, payload, targets):
        """

        :param payload:
        :param targets:
        :return:
        """
        # 华为推送接口请求参数
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        nsp_ctx = '{{"ver":"{0}", "appId":"{1}"}}'.format(self.ver, self.app_id)
        # 创建时间戳，华为的服务器时间似乎有些误差，需要加一分钟才能正常通过验证
        now = datetime.now() + relativedelta(minutes=1)
        utc_time = calendar.timegm(now.timetuple())
        device_token_list = json.dumps(targets)
        local_time = now.strftime("%Y-%m-%dT%H:%M")
        request_msg = {'access_token': self.token, 'nsp_svc': 'openpush.message.api.send',
                       'nsp_ts': utc_time, 'expire_time': local_time,
                       'device_token_list': device_token_list}
        request_msg.update({'payload': json.dumps(payload)})
        resp = WebRequests.requests(method='post', headers=headers,
                                    query_string={'nsp_ctx': nsp_ctx},
                                    url=self.push_url,
                                    data=request_msg)
        return resp

if __name__ == '__main__':
    pass
