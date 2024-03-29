#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : EXP
# @Time   : 2020/8/11 22:17
# -----------------------------------------------

import argparse
import sys
import re
import time
import datetime
from src.config import *
from color_log.clog import log
from src.utils import _git
from src.builder import weektime
from src.builder import activity
from src.builder import article


sys.stdout.reconfigure(encoding=CHARSET)
README_PATH = '%s/README.md' % PRJ_DIR


def args() :
    parser = argparse.ArgumentParser(
        prog='', # 会被 usage 覆盖
        usage='python main.py -g {Github Token} -p {http://PROXY_IP:PORT}',  
        description='自动更新 Github Profile 的每日动态脚本',  
        epilog='\r\n'.join([
            '更多参数执行', 
            '  python main.py -h', 
            '查看', 
        ])
    )
    parser.add_argument('-g', '--gtk', dest='gtk', type=str, default="", help='Github Token， 用于 GraphQL 查询')
    parser.add_argument('-p', '--proxy', dest='proxy', type=str, default="", help='代理服务，如： http://127.0.0.1:18888, socks5://127.0.0.1:1088')
    return parser.parse_args()



def get_args(args) :
    github_token = args.gtk or settings.github['gtk']
    proxy = args.proxy or settings.github['proxy']
    return [ github_token, proxy ]



def main(github_token, proxy):
    log.info("正在读取 [README.md] ...")
    with open(README_PATH, 'r', encoding=CHARSET) as file :
        readme = file.read()

    log.info("正在读取所有项目仓库的活动数据 ...")
    repos = []
    repos.extend(_git.query_repos(github_token, 'master'))
    repos.extend(_git.query_repos(github_token, 'main'))    # 兼容主分支为 main 情况
    repos.sort(reverse=True, key=lambda repo: int(time.mktime(
        datetime.datetime.strptime(repo.pushtime, "%Y-%m-%d %H:%M:%S").timetuple()
    )))
    
    if not repos or len(repos) <= 0 :
        log.warn("获取项目仓库数据失败")
    else :
        log.info("获得 [%i] 个项目仓库的数据" % len(repos))

        log.info("正在构造 [时间分配] 数据 ...")
        try :
            data_wt = weektime.build(repos)
            readme = reflash(readme, data_wt, 'weektime')
            log.info(data_wt)
        except :
            log.error("构造数据异常")

        log.info("正在构造 [最近活跃] 数据 ...")
        try :
            data_ac = activity.build(repos, settings.app['activity_num'])
            readme = reflash(readme, data_ac, 'activity')
            log.info(data_ac)
        except :
            log.error("构造数据异常")

    log.info("正在构造 [最新文章] 数据 ...")
    try :
        data_ar = article.build(github_token, proxy)
        readme = reflash(readme, data_ar, 'article')
        log.info(data_ar)
    except :
        log.error("构造数据异常")

    log.info("正在更新 [README.md] ...")
    with open(README_PATH, 'w', encoding=CHARSET) as file :
        file.write(readme)
    log.info("已更新 [README.md]")



def reflash(readme, data, tag) :
    TAG_BGN = '<!-- BGN_SECTION:%s -->' % tag
    TAG_END = '<!-- END_SECTION:%s -->' % tag
    RGX = '%s(.+?)%s' % (TAG_BGN, TAG_END)
    ptn = re.compile(RGX, re.DOTALL)
    mth = re.search(ptn, readme)
    if mth :
        readme = readme.replace(mth.group(1), data)
    return readme



if __name__ == '__main__':
    main(*get_args(args()))
