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
        request_body = self.__request_body(
            query=query, variables=variables, operation_name=operation_name
        )

        proxies = { "http": proxy, "https": proxy } if proxy else {}
        result = requests.post(
            self.endpoint, 
            json=request_body, 
            headers=self.__request_headers(headers),
            proxies=proxies
        )

        result.raise_for_status()
        return result.json()
