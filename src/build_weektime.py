#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : EXP
# @Time   : 2020/8/11 22:17
# -----------------------------------------------


TOPIC_WRITING = 'writing'
TOPIC_LEARNING = 'learning'
TOPIC_PROGRAMMING = 'programming'
TOPIC_PLAYING = 'playing'

BIT_WRITING = 1
BIT_LEARNING = 2
BIT_PROGRAMMING = 4
BIT_PLAYING = 8

def load_weektime(repos) :
    cnt_writing = 0
    cnt_learning = 0
    cnt_programming = 0
    cnt_playing = 0
    cnt_other = 0

    for repo in repos :
        if repo.is_for_writing() :
            cnt_writing += repo.commit_cnt
        elif repo.is_for_learning() :
            cnt_learning += repo.commit_cnt
        elif repo.is_for_programming() :
            cnt_programming += repo.commit_cnt
        elif repo.is_for_playing() :
            cnt_playing += repo.commit_cnt
        else :
            cnt_other += repo.commit_cnt

    total = cnt_writing + cnt_learning + cnt_programming + cnt_playing + cnt_other
    print('%i / %i' % (cnt_writing, total))
    print('%i / %i' % (cnt_learning, total))
    print('%i / %i' % (cnt_programming, total))
    print('%i / %i' % (cnt_playing, total))
    print('%i / %i' % (cnt_other, total))


