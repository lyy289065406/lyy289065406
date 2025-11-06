#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : EXP
# @Time   : 2020/4/28 21:56
# -----------------------------------------------
# https://developer.github.com/v4/object/repository/
# -----------------------------------------------

import requests
from python_graphql_client import GraphqlClient

# 重载 GraphqlClient 类，增加代理支持
class _GraphqlClient(GraphqlClient) :

    def exec(
        self,
        query: str,
        variables: dict = None,
        operation_name: str = None,
        headers: dict = None,
        proxy: str = ''
    ):
        """Make synchronous request to graphQL server."""
        # 使用新版本的 execute 方法
        headers = headers or {}
        # 自动添加 http:// 前缀（如果没有的话）
        if proxy and not proxy.startswith(('http://', 'https://')):
            proxy = f"http://{proxy}"
        proxies = { "http": proxy, "https": proxy } if proxy else {}
        
        return self.execute(
            query=query,
            variables=variables,
            operation_name=operation_name,
            headers=headers,
            proxies=proxies
        )
