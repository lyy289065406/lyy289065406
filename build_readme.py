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
GITHUB_REPO = 'threat-broadcast'
GITHUB_REPO_OWNER = 'lyy289065406'

def _to_graphql(next_cursor, owner, repo, iter):
    return ("""
query {
  viewer {
    repositories(first: 100, orderBy: {field: PUSHED_AT, direction: DESC}, isFork: false, after: null) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        name
        description
        url
        createdAt
        pushedAt
        object(expression: "master") {
          ... on Commit {
            history(first: 3) {
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
""").replace(
        "NEXT", '"{}"'.format(next_cursor) if next_cursor else "null"
    )


def query_issues(github_token, owner=GITHUB_REPO_OWNER, repo=GITHUB_REPO, iter=100):
    titles = []
    client = GraphqlClient(endpoint=GITHUB_GRAPHQL)
    has_next_page = True
    next_cursor = None
    while has_next_page:
        data = client.execute(
            query=_to_graphql(next_cursor, owner, repo, iter),
            headers={ "Authorization": "Bearer {}".format(github_token) },
        )
        print(json.dumps(data))

        pageInfo = data["data"]["viewer"]["repositories"]["pageInfo"]
        has_next_page = pageInfo["hasNextPage"]
        next_cursor = pageInfo["endCursor"]
    return titles


def main(help, github_token):
    #TODO 更新 Github Repo、Blog 状态到 README
    query_issues(github_token)



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

