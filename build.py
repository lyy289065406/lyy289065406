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


def main(help, github_token):
    repos = _git.query_repos(github_token)
    table_wt = weektime.build(repos)
    table_ac = activity.build(repos)
    table_ar = article.build(github_token)



def reflash(data, tag) :
    TAG_BGN = '<!-- BGN_SECTION:%s -->' % tag
    TAG_END = '<!-- END_SECTION:%s -->' % tag
    RGX = '%s([\s|S]+?)%s' % (TAG_BGN, TAG_END)
    



def get_sys_args(sys_args) :
    help = False
    github_token = ''

    idx = 1
    size = len(sys_args)
    while idx < size :
        try :
            if sys_args[idx] == '-h' :
                help = True

            elif sys_args[idx] == '-gtk' :
                idx += 1
                github_token = sys_args[idx]

        except :
            pass
        idx += 1
    return help, github_token



if __name__ == '__main__':
    main(*get_sys_args(sys.argv))
