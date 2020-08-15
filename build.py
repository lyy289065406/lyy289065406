#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : EXP
# @Time   : 2020/8/11 22:17
# -----------------------------------------------

import sys
import json
from python_graphql_client import GraphqlClient
from src.builder import weektime






def main(help, github_token):
    repos = query_repos(github_token)
    print(weektime.build(repos))
    #TODO 更新 Github Repo、Blog 状态到 README
    


def load_activity() :
    pass


def load_articles() :
    pass





TOPIC_WRITING = 'writing'
TOPIC_PROGRAMMING = 'programming'
TOPIC_PLAYING = 'playing'
TOPIC_LEARNING = 'learning'

BIT_WRITING = 1
BIT_PROGRAMMING = 2
BIT_PLAYING = 4
BIT_LEARNING = 8

class Repo :

    def __init__(self, name, url, desc, pushtime, commit_cnt) :
        self.name = name
        self.url = url
        self.desc = desc
        self.pushtime = pushtime
        self.commit_cnt = commit_cnt
        self.topics = []
        self.usefor = 0


    def add_topic(self, topic) :
        if topic is None :
            return
        self.topics.append(topic)

        if TOPIC_WRITING == topic.lower() :
            self.usefor |= BIT_WRITING

        elif TOPIC_PROGRAMMING == topic.lower() :
            self.usefor |= BIT_PROGRAMMING

        elif TOPIC_PLAYING == topic.lower() :
            self.usefor |= BIT_PLAYING

        else :
            self.usefor |= BIT_LEARNING


    def is_for_writing(self) :
        return (self.usefor & BIT_WRITING) != 0


    def is_for_learning(self) :
        return (self.usefor & BIT_LEARNING) != 0 


    def is_for_programming(self) :
        return (self.usefor & BIT_PROGRAMMING) != 0 


    def is_for_playing(self) :
        return (self.usefor & BIT_PLAYING) != 0 


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

