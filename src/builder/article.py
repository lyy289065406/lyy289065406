#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : EXP
# @Time   : 2020/8/11 22:17
# -----------------------------------------------

import os
import requests
import re
import time
from src.cfg.env import *


PROXY_TROJAN = 'http://127.0.0.1:8888'
TPL_PATH = '%s/tpl/article.tpl' % PRJ_DIR
SAVE_PATH = PRJ_DIR + '/cache/article_%s.dat'

EXP_BLOG_REPO = 'exp-blog'
EXP_BLOG_SITEMAP = 'https://exp-blog.com/gitbook/book/sitemap.xml'

RE0_WEB_REPO = 're0-web'
RE0_WEB_SITEMAP = 'https://lyy289065406.github.io/re0-web/gitbook/book/sitemap.xml'



def build(repos) :
    ar = ArticleRefresher(EXP_BLOG_REPO, EXP_BLOG_SITEMAP, PROXY_TROJAN)
    ar.reflash()
    row = ar.get_top1()
    print(row)

    ar = ArticleRefresher(RE0_WEB_REPO, RE0_WEB_SITEMAP, PROXY_TROJAN)
    ar.reflash()
    row = ar.get_top1()
    print(row)



class ArticleRefresher :

    def __init__(self, repo_name, sitemap_url, proxy='', timeout=60, charset=CHARSET) :
        self.repo_name = repo_name
        self.sitemap_url = sitemap_url
        self.save_path = SAVE_PATH % self.repo_name
        self.save_cache = []
        self.charset = charset
        self.timeout = timeout
        self.proxies = { "http": proxy, "https": proxy } if proxy else {}


    def reflash(self) :
        self._load()
        rsp = requests.get(
            self.sitemap_url, 
            headers = self._headers(), 
            timeout = self.timeout,
            proxies = self.proxies
        )
        if rsp.status_code == 200 :
            urls = re.findall('<loc>(.+?\.html)</loc>', rsp.text)
            for url in urls :
                if url not in self.save_cache :
                    self.save_cache.insert(0, url)
        self._save()


    def get_topN(self, top=1) :
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        with open(TPL_PATH, 'r') as file :
            tpl = file.read()
            top1 = tpl % {
                'repo': self.repo_name, 
                'repo_url': '', 
                'article': self._get_top1_title(), 
                'article_url': '', 
                'time': now, 
                'new_flag': NEW_FLAG
            }
        return top1


    def _get_top_urls(self) :
        return self.save_cache[0] if len(self.save_cache) > 0 else ''


    def _get_top_titles(self) :
        rsp = requests.get(
            self._get_top1_url(), 
            headers = self._headers(), 
            timeout = self.timeout,
            proxies = self.proxies
        )
        if rsp.status_code == 200 :
            rst = re.findall('<h1 id=".+?">(.+?)</h1>', rsp.text)
            title = rst[0] if len(rst) > 0 else ''
        return title


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




class Article :

    def __init__(self, title, url) :
        self.title = title
        self.url = url

