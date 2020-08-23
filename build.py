#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : EXP
# @Time   : 2020/8/11 22:17
# -----------------------------------------------

import sys
import json
import re
from src.cfg.env import *
from src.utils import _git
from src.builder import weektime
from src.builder import activity
from src.builder import article


README_PATH = '%s/README.md' % PRJ_DIR


def main(help, github_token, proxy):
    repos = _git.query_repos(github_token)
    data_wt = weektime.build(repos)
    data_ac = activity.build(repos)
    data_ar = article.build(github_token, proxy)

    with open(README_PATH, 'r', encoding=CHARSET) as file :
        readme = file.read()
        readme = reflash(readme, data_wt, 'weektime')
        readme = reflash(readme, data_ac, 'activity')
        readme = reflash(readme, data_ar, 'article')

    with open(README_PATH, 'w', encoding=CHARSET) as file :
        file.write(readme)



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
    main(*get_sys_args(sys.argv))
