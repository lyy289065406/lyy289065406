#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : EXP
# @Time   : 2020/8/11 22:17
# -----------------------------------------------

import math
from src.cfg.env import *

TPL_PATH = '%s/tpl/weektime.tpl' % PRJ_DIR


def build(repos) :
    cnt_writing = 0
    cnt_programming = 0
    cnt_playing = 0
    cnt_learning = 0

    for repo in repos :
        if repo.is_for_writing() :
            cnt_writing += repo.commit_cnt
        elif repo.is_for_programming() :
            cnt_programming += repo.commit_cnt
        elif repo.is_for_playing() :
            cnt_playing += repo.commit_cnt
        else :
            cnt_learning += repo.commit_cnt

    cnt_total = cnt_writing + cnt_programming + cnt_playing + cnt_learning
    percent_wr = cnt_writing / cnt_total
    percent_pr = cnt_programming / cnt_total
    percent_pl = cnt_playing / cnt_total
    percent_ln = cnt_learning / cnt_total

    hour_wr = to_hour(percent_wr)
    hour_pr = to_hour(percent_pr)
    hour_pl = to_hour(percent_pl)
    hour_ln = to_hour(percent_ln)
    
    progress_wr = to_progress(percent_wr)
    progress_pr = to_progress(percent_pr)
    progress_pl = to_progress(percent_pl)
    progress_ln = to_progress(percent_ln)

    content = ''
    with open(TPL_PATH, 'r') as file :
        tpl = file.read()
        content = tpl % {
            'hour_wr': hour_wr, 
            'hour_pr': hour_pr,
            'hour_pl': hour_pl,
            'hour_ln': hour_ln,
            'progress_wr': progress_wr,
            'progress_pr': progress_pr,
            'progress_pl': progress_pl,
            'progress_ln': progress_ln,
            'percent_wr': '{:06.2%}'.format(percent_wr),
            'percent_pr': '{:06.2%}'.format(percent_pr),
            'percent_pl': '{:06.2%}'.format(percent_pl),
            'percent_ln': '{:06.2%}'.format(percent_ln)
        }
    return content



def to_hour(percent) :
    hour_total = 40
    hour = math.ceil(hour_total * percent)
    return '%02d' % hour


def to_progress(percent) :
    BLACK = 'o'
    WHITE = 'x'
    cnt = math.ceil(percent * 10) * 2
    return '%s%s' % (BLACK * cnt, WHITE * (20 - cnt))
