#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : EXP
# @Time   : 2020/8/11 22:17
# -----------------------------------------------

import sys
import re
from src.cfg.env import *
from src.utils import log
from src.utils import _git
from src.builder import weektime
from src.builder import activity
from src.builder import article


README_PATH = '%s/README.md' % PRJ_DIR


def main(help, github_token, proxy):
    if help == True :
        log.info(help_info())

    else :
        log.info("正在读取 [README.md] ...")
        with open(README_PATH, 'r', encoding=CHARSET) as file :
            readme = file.read()

        log.info("正在读取所有项目仓库的活动信息 ...")
        repos = _git.query_repos(github_token)

        if repos and len(repos) > 0 :
            log.info("正在构造 [时间分配] 数据 ...")
            try :
                data_wt = weektime.build(repos)
                readme = reflash(readme, data_wt, 'weektime')
            except :
                log.error("构造数据异常")

            log.info("正在构造 [最近活跃] 数据 ...")
            try :
                data_ac = activity.build(repos)
                readme = reflash(readme, data_ac, 'activity')
            except :
                log.error("构造数据异常")

        log.info("正在构造 [最新文章] 数据 ...")
        try :
            data_ar = article.build(github_token, proxy)
            readme = reflash(readme, data_ar, 'article')
        except :
            log.error("构造数据异常")

        log.info("正在更新 [README.md] ...")
        with open(README_PATH, 'w', encoding=CHARSET) as file :
            file.write(readme)



def help_info():
    return '''
    -h                   帮助信息
    -gtk                 Github Token， 用于 GraphQL 查询
    -proxy <http/https>  代理服务，如： http://127.0.0.1:8888
'''



def reflash(readme, data, tag) :
    TAG_BGN = '<!-- BGN_SECTION:%s -->' % tag
    TAG_END = '<!-- END_SECTION:%s -->' % tag
    RGX = '%s(.+?)%s' % (TAG_BGN, TAG_END)
    ptn = re.compile(RGX, re.DOTALL)
    mth = re.search(ptn, readme)
    if mth :
        readme = readme.replace(mth.group(1), data)
    return readme



def get_sys_args(sys_args) :
    help = False
    github_token = ''
    proxy = ''

    idx = 1
    size = len(sys_args)
    while idx < size :
        try :
            if sys_args[idx] == '-h' :
                help = True

            elif sys_args[idx] == '-gtk' :
                idx += 1
                github_token = sys_args[idx]

            elif sys_args[idx] == '-proxy' :
                idx += 1
                proxy = sys_args[idx]

        except :
            pass
        idx += 1
    return help, github_token, proxy



if __name__ == '__main__':
    log.init()
    main(*get_sys_args(sys.argv))
