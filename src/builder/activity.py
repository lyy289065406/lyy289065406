#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : EXP
# @Time   : 2020/8/11 22:17
# -----------------------------------------------

from src.config import *
import re

TPL_PATH = '%s/tpl/activity.tpl' % PRJ_DIR

def build(repos, top=3) :
    with open(TPL_PATH, 'r') as file :
        tpl = file.read().rstrip('\r\n')

    rows = []
    cnt = 0
    for repo in repos :
        if is_skip(repo.name) :
            continue

        row = tpl % {
            'repo': repo.name, 
            'repo_url': repo.url, 
            'visibility': '公开' if repo.visibility == 'PUBLIC' else '非公开',
            'desc': repo.desc, 
            'count': repo.commit_cnt, 
            'time': repo.pushtime, 
            'new_flag': settings.app['new_flag_img'] if cnt == 0 else ''
        }
        rows.append(row)

        cnt += 1
        if cnt >= top :
            break

    return """
| repo | visibility | description | commit count | push time |
|:------|:------|:------|:------|:------|
%s
""" % '\n'.join(rows)


def is_skip(repo_name) :
    is_found = False
    for feature in settings.skip_repos :
        if repo_name == feature :
            is_found = True
            break

        if re.match(feature, repo_name, re.I) :
            is_found = True
            break
    return is_found
