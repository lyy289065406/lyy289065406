#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : EXP
# @Time   : 2020/8/11 22:17
# -----------------------------------------------

import requests
import re
import time
from src.cfg.env import *
from src.utils import _git


MODE_RSS = 'rss'
MODE_SITEMAP = 'sitemap'

TPL_PATH = '%s/tpl/article.tpl' % PRJ_DIR
SAVE_PATH = PRJ_DIR + '/cache/article_%s.dat'

EXP_BLOG_REPO = 'articles'
EXP_BLOG_URL = 'https://exp-blog.com/atom.xml'

RE0_WEB_REPO = 're0-web'
RE0_WEB_URL = 'https://lyy289065406.github.io/re0-web/gitbook/book/sitemap.xml'



def build(github_token, proxy='') :
    rows = []

    ar = ArticleRefresher(github_token, EXP_BLOG_REPO, EXP_BLOG_URL, proxy)
    # ar.reflash()      # RSS 会自动排序，不需要缓存到本地
    rows.extend(ar.get_tops(MODE_RSS, 2))

    ar = ArticleRefresher(github_token, RE0_WEB_REPO, RE0_WEB_URL, proxy)
    ar.reflash()        # sitemap 无序，需要缓存到本地
    rows.extend(ar.get_tops(MODE_SITEMAP, 1))

    return """
| repo | article | push time |
|:------|:------|:------|
%s
""" % '\n'.join(rows)



class ArticleRefresher :

    def __init__(self, github_token, repo_name, url, proxy='', timeout=60, charset=CHARSET) :
        self.gtk = github_token
        self.repo_name = repo_name
        self.github_url = GITHUB_URL + repo_name
        self.url = url
        self.save_path = SAVE_PATH % self.repo_name
        self.save_cache = []
        self.charset = charset
        self.timeout = timeout
        self.proxies = { "http": proxy, "https": proxy } if proxy else {}


    def reflash(self) :
        self._load()
        rsp = requests.get(
            self.url, 
            headers = self._headers(), 
            timeout = self.timeout,
            proxies = self.proxies
        )
        if rsp.status_code == 200 :
            urls = re.findall(r'<loc>(.+?\.html)</loc>', rsp.text)
            for url in urls :
                if url not in self.save_cache :
                    self.save_cache.insert(0, url)
        self._save()


    def get_tops(self, mode, top=1) :
        tops = []
        with open(TPL_PATH, 'r') as file :
            tpl = file.read()

            cnt = 0
            articles = self._get_top_articles(mode, top)
            for article in articles :
                tops.append(tpl % {
                    'repo': self.repo_name, 
                    'repo_url': self.github_url, 
                    'article': article.title, 
                    'article_url': article.url, 
                    'time': article.time, 
                    'new_flag': NEW_FLAG if cnt == 0 else ''
                })
                cnt += 1
        return tops


    def _get_top_articles(self, mode, top) :
        articles = []

        if mode == MODE_SITEMAP :
            urls = self._get_top_urls(top)
            for url in urls :
                rsp = requests.get(
                    url, 
                    headers = self._headers(), 
                    timeout = self.timeout,
                    proxies = self.proxies
                )
                if rsp.status_code == 200 :
                    rst = re.findall(r'<h1 id=".+?">(.+?)</h1>', rsp.text)
                    title = rst[0].strip() if len(rst) > 0 else ''
                    title = re.sub(r'.*</a>', '', title)
                    time = self._query_filetime(url)
                    article = Article(title, url, time)
                    articles.append(article)

        elif mode == MODE_RSS :
            rsp = requests.get(
                self.url, 
                headers = self._headers(), 
                timeout = self.timeout,
                proxies = self.proxies
            )
            rsp.encoding = 'utf-8'
            if rsp.status_code == 200 :
                titles = re.findall(r'<title>(.+?)</title>', rsp.text)
                urls = re.findall(r'<id>(.+?)</id>', rsp.text)
                times = re.findall(r'<published>(.+?)</published>', rsp.text)
                for i in range(top) :
                    title = titles[i + 1]
                    url = urls[i + 1]
                    time = times[i].replace('T', ' ').replace('.000Z', '')
                    article = Article(title, url, time)
                    articles.append(article)

        return articles


    def _get_top_urls(self, top=1) :
        return self.save_cache[:top]


    def _query_filetime(self, file_url) :
        filepath = self._to_filepath(file_url)
        return _git.query_filetime(self.gtk, self.repo_name, filepath)


    def _to_filepath(self, file_url) :
        return re.sub(r'.*?/markdown', 'gitbook/markdown', file_url.replace('.html', '.md'))


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

    def __init__(self, title, url, time) :
        self.title = title
        self.url = url
        self.time = time

