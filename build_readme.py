#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : EXP
# @Time   : 2020/8/11 22:17
# @File   : main.py
# -----------------------------------------------

import sys
import json
from python_graphql_client import GraphqlClient

GITHUB_GRAPHQL = 'https://api.github.com/graphql'
GITHUB_REPO_OWNER = 'lyy289065406'

TOPIC_WRITING = 'writing'
TOPIC_LEARNING = 'learning'
TOPIC_PROGRAMMING = 'programming'
TOPIC_PLAYING = 'playing'

BIT_WRITING = 1
BIT_LEARNING = 2
BIT_PROGRAMMING = 4
BIT_PLAYING = 8


def main(help, github_token):
    repos = query_repos(github_token)
    #TODO 更新 Github Repo、Blog 状态到 README
    


def load_weektime(repos) :
    cnt_writing = 0
    cnt_learning = 0
    cnt_programming = 0
    cnt_playing = 0
    cnt_other = 0

    for repo in repos :
        if repo.is_for_writing :
            cnt_writing += repo.commit_cnt
        elif repo.is_for_learning :
            cnt_learning += repo.commit_cnt
        elif repo.is_for_programming :
            cnt_programming += repo.commit_cnt
        elif repo.is_for_playing :
            cnt_playing += repo.commit_cnt
        else :
            cnt_other += repo.commit_cnt

    total = cnt_writing + cnt_learning + cnt_programming + cnt_playing + cnt_other
    print('%i / %i' % (cnt_writing, total))
    print('%i / %i' % (cnt_learning, total))
    print('%i / %i' % (cnt_programming, total))
    print('%i / %i' % (cnt_playing, total))
    print('%i / %i' % (cnt_other, total))
        


def load_activity() :
    pass


def load_articles() :
    pass


def query_repos(github_token, iter=100):
    repos = []
    client = GraphqlClient(endpoint=GITHUB_GRAPHQL)
    has_next_page = True
    next_cursor = None
    while has_next_page:
        data = client.execute(
            query=_to_graphql(next_cursor, iter),
            headers={ "Authorization": "Bearer {}".format(github_token) },
        )
        
        _repos = data["data"]["viewer"]["repositories"]["nodes"]
        for _repo in _repos :
            repo = Repo(
                _repo["name"], 
                _repo["url"], 
                _repo["description"], 
                _repo["pushedAt"], 
                _repo["object"]["history"]["totalCount"]
            )
            topics = _repo["repositoryTopics"]["nodes"]
            for topic in topics :
                repo.add_topic(topic["topic"]["name"])
            repos.append(repo)

        pageInfo = data["data"]["viewer"]["repositories"]["pageInfo"]
        has_next_page = pageInfo["hasNextPage"]
        next_cursor = pageInfo["endCursor"]
    return repos


def _to_graphql(next_cursor, iter):
    return """
query {
  viewer {
    repositories(first: 50, orderBy: {field: PUSHED_AT, direction: DESC}, isFork: false, after: null) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        name
        description
        url
        pushedAt
        repositoryTopics(first: 5) {
          nodes {
              topic {
                name
              }
          }
        }
        object(expression: "master") {
          ... on Commit {
            history(first: 2) {
              totalCount
              nodes {
                committedDate
                message
              }
            }
          }
        }
      }
    }
  }
}
""".replace(
        "NEXT", '"{}"'.format(next_cursor) if next_cursor else "null"
    )



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

        elif TOPIC_LEARNING == topic.lower() :
            self.usefor |= BIT_LEARNING

        elif TOPIC_PROGRAMMING == topic.lower() :
            self.usefor |= BIT_PROGRAMMING

        elif TOPIC_PLAYING == topic.lower() :
            self.usefor |= BIT_PLAYING


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

