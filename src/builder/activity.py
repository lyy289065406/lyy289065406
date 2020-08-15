#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : EXP
# @Time   : 2020/8/11 22:17
# -----------------------------------------------

from src.cfg.env import *

TPL_PATH = '%s/tpl/activity.tpl' % PRJ_DIR
NEW_FLAG = '![news](https://github.com/lyy289065406/lyy289065406/blob/master/imgs/new.gif)'
GITHUB_REPO_OWNER = 'lyy289065406'
TOP = 3

def build(repos) :
    with open(TPL_PATH, 'r') as file :
        tpl = file.read()

    rows = []
    cnt = 0
    for repo in repos :
        if repo.name == GITHUB_REPO_OWNER :
            continue

        row = tpl % {
            'repo': repo.name, 
            'count': repo.commit_cnt, 
            'time': repo.pushtime, 
            'new_flag': NEW_FLAG if cnt == 0 else ''
        }
        rows.append(row)

        cnt += 1
        if cnt >= TOP :
            break

    return '\n'.join(rows)

