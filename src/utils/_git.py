#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : EXP
# @Time   : 2020/4/28 21:56
# -----------------------------------------------

from src.cfg.env import *
from src.bean.repo import *
from python_graphql_client import GraphqlClient



def query_repos(github_token, iter=100):
    repos = []
    client = GraphqlClient(endpoint=GITHUB_GRAPHQL)
    has_next_page = True
    next_cursor = None
    while has_next_page:
        data = client.execute(
            query=_to_graphql_repoinfo(next_cursor, iter),
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


def _to_graphql_repoinfo(next_cursor, iter):
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
            history(first: 1) {
              totalCount
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




def query_filetime(github_token, repo, filepath):
    client = GraphqlClient(endpoint=GITHUB_GRAPHQL)
    data = client.execute(
        query=_to_graphql_filetime(GITHUB_OWNER, repo, filepath),
        headers={ "Authorization": "Bearer {}".format(github_token) },
    )
    fileinfo = data["repository"]["object"]["blame"]["ranges"]
    filetime = fileinfo[0]["commit"]["committedDate"]
    return filetime


def _to_graphql_filetime(owner, repo, filepath) :
  return """
query {
  repository(owner: "%s", name: "%s") {
    object(expression: "master") {
      ... on Commit {
        blame(path: "%s") {
          ranges {
            commit {
              committedDate
            }
          }
        }
      }
    }
  }
}
""" % (owner, repo, filepath)
