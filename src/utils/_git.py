#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : EXP
# @Time   : 2020/4/28 21:56
# -----------------------------------------------

from src.bean.repo import *
from python_graphql_client import GraphqlClient

GITHUB_GRAPHQL = 'https://api.github.com/graphql'


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
    repositories(first: 100, orderBy: {field: PUSHED_AT, direction: DESC}, isFork: false, after: NEXT) {
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

