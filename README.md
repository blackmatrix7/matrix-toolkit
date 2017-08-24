# Matirx Tookit
一些方便日常使用的小工具，及制造过的小轮子。

#### [config](https://github.com/blackmatrix7/matirx-tookit/blob/master/config.py)

实现部分dict协议的配置操作混合类（Mixin），简化配置文件的读取与继承。

#### [cache](https://github.com/blackmatrix7/matirx-tookit/blob/master/cache/cache.py)

基于Python3-memcached的浅封装，支持在key之前加入统一的前缀，提供两个函数装饰器：cached() 用于缓存函数执行结果， delcache()用于在函数执行完成后清理缓存。

#### **[retry](https://github.com/blackmatrix7/matirx-tookit/blob/master/decorator/retry.py)**

在函数执行出现异常时自动重试的简单装饰器，支持设定每次重试间隔时间，及每次重试间隔时间递增。