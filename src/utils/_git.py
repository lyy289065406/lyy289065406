#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : EXP
# @Time   : 2020/4/28 21:56
# -----------------------------------------------

import requests
from color_log.clog import log
from src.config import *
from src.bean.repo import *
from src.utils.graphql_client import _GraphqlClient


def query_repos(github_token, branch='master', iter=100, proxy=''):
    repos = []
    client = _GraphqlClient(endpoint=settings.github['graphql'])
    has_next_page = True
    next_cursor = None
    while has_next_page:
        data = client.exec(
            query=_to_graphql_repoinfo(branch, next_cursor, iter),
            headers={ "Authorization": "Bearer {}".format(github_token) },
            proxy=proxy
        )
        # log.debug(data)
        _repos = data["data"]["viewer"]["repositories"]["nodes"]
        for _repo in _repos :
            if _repo["object"] is None :
                continue  # 不存在的分支名

            repo = Repo(
                _repo["owner"]["login"], 
                _repo["name"], 
                _repo["url"], 
                _repo["description"], 
                _utc_to_local(_repo["pushedAt"]), 
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



def _to_graphql_repoinfo(branch, next_cursor, iter):
    return """
query {
  viewer {
    repositories(first: ITER, orderBy: {field: PUSHED_AT, direction: DESC}, isFork: false, after: NEXT) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        owner {
          __typename
          ... on User {
            login
          }
          ... on Organization {
            login
          }
        }
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
        object(expression: "BRANCH") {
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
""".replace("BRANCH", branch).replace("ITER", str(iter)).replace(
    "NEXT", '"{}"'.format(next_cursor) if next_cursor else "null"
)




def query_filetime(github_token, repo_owner, repo_name, filepath, proxy=''):
    """通过 REST API 查询文件最后提交时间，比 GraphQL blame/commitHistory 更稳定"""
    url = f"{settings.github['url'].replace('https://github.com', 'https://api.github.com')}/repos/{repo_owner}/{repo_name}/commits"
    headers = {
        "Authorization": "Bearer {}".format(github_token),
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "python"
    }
    proxies = { "http": proxy, "https": proxy } if proxy else {}
    params = { "path": filepath, "page": 1, "per_page": 1 }
    rsp = requests.get(url, headers=headers, params=params, proxies=proxies, timeout=30)
    rsp.raise_for_status()
    commits = rsp.json()
    if not commits:
        raise ValueError(f"No commits found for {filepath}")
    filetime = commits[0]["commit"]["committer"]["date"]
    return _utc_to_local(filetime)



def _utc_to_local(utc) :
    return utc.replace('T', ' ').replace('Z', '')

