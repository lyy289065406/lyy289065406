#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : EXP
# @Time   : 2020/8/11 22:17
# -----------------------------------------------

from src.config import *

TPL_PATH = '%s/tpl/activity.tpl' % PRJ_DIR

def build(repos, top=3) :
    with open(TPL_PATH, 'r') as file :
        tpl = file.read()

    rows = []
    cnt = 0
    for repo in repos :
        if repo.name in settings.skip_repos :
            continue

        row = tpl % {
            'repo': repo.name, 
            'repo_url': repo.url, 
            'count': repo.commit_cnt, 
            'time': repo.pushtime, 
            'new_flag': settings.app['new_flag_img'] if cnt == 0 else ''
        }
        rows.append(row)

        cnt += 1
        if cnt >= top :
            break

    return """
| repo | commit count | push time |
|:------|:------|:------|
%s
""" % '\n'.join(rows)

