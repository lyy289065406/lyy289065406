#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : EXP
# @Time   : 2020/8/11 22:17
# -----------------------------------------------

import os
import requests
import re
from src.cfg.env import *


EXP_BLOG_SITEMAP = 'http://exp-blog.com/gitbook/book/sitemap.xml'
EXP_BLOG_SAVE_PATH = '%s/cache/article_exp_blog.dat' % PRJ_DIR
EXP_BLOG_SAVE_CACHE = []

RE0_WEB_SITEMAP = 'http://lyy289065406.github.io/re0-web/gitbook/book/sitemap.xml'
RE0_WEB_SAVE_PATH = '%s/cache/article_re0_web.dat' % PRJ_DIR
RE0_WEB_SAVE_CACHE = []


def build(repos) :
    # ar = ArticleRefresher(EXP_BLOG_SITEMAP, EXP_BLOG_SAVE_PATH, EXP_BLOG_SAVE_CACHE)
    # ar.reflash()
    # url = ar.take_newly()
    # print(url)

    ar = ArticleRefresher(RE0_WEB_SITEMAP, RE0_WEB_SAVE_PATH, RE0_WEB_SAVE_CACHE)
    ar.reflash()
    url = ar.take_newly()
    print(url)



class ArticleRefresher :

    def __init__(self, sitemap_url, save_path, save_cache, charset=CHARSET, timeout=60) :
        self.sitemap_url = sitemap_url
        self.save_path = save_path
        self.save_cache = save_cache
        self.charset = charset
        self.timeout = timeout


    def reflash(self) :
        self._load()
        rsp = requests.get(
            self.sitemap_url, 
            headers = self._headers(), 
            timeout = self.timeout,
            proxies = {}
        )
        if rsp.status_code == 200 :
            urls = re.findall('<loc>(.+\.html)</loc>', rsp.text)
            for url in urls :
                if url not in self.save_cache :
                    self.save_cache.insert(0, url)
        self._save()


    def take_newly(self) :
        return self.save_cache[0] if len(self.save_cache) > 0 else ''


    def _headers(self):
        return {
            'Accept' : '*/*',
            'Accept-Encoding' : 'gzip, deflate, br',
            'Accept-Language' : 'zh-CN,zh;q=0.9',
            'Connection' : 'keep-alive',
            'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        }


    def _load(self) :
        if os.path.exists(self.save_path) :
            with open(self.save_path, 'r', encoding=self.charset) as file :
                lines = file.readlines()
                for line in lines :
                    self.save_cache.append(line.strip())


    def _save(self) :
        with open(self.save_path, 'w+', encoding=self.charset) as file :
            file.write('\n'.join(self.save_cache))


