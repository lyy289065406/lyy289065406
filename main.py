#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : EXP
# @Time   : 2020/4/25 22:17
# @File   : main.py
# -----------------------------------------------

from python_graphql_client import GraphqlClient
import pathlib
import os
import json

PRJ_ROOT = pathlib.Path(__file__).parent.resolve()
client = GraphqlClient(endpoint="https://api.github.com/graphql")
TOKEN = os.environ.get("GRAPHQL_TOKEN", "")

def make_query(after_cursor=None):
    return """
query {
    repository(owner: "lyy289065406", name: "threat-broadcast") {
        issues(orderBy:{field: UPDATED_AT, direction: DESC} , labels: null, first: 10, after: AFTER) {
            edges{
                node {
                    title
                    updatedAt
                    bodyText
                    number
                }
            }
            pageInfo {
                hasNextPage
                endCursor
            }
        }
    }
}
""".replace(
        "AFTER", '"{}"'.format(after_cursor) if after_cursor else "null"
    )

def fetch_releases(oauth_token):
    repos = []
    releases = []
    repo_names = set()
    has_next_page = True
    after_cursor = None

    while has_next_page:
        data = client.execute(
            query=make_query(after_cursor),
            headers={"Authorization": "Bearer {}".format(oauth_token)},
        )
        print(data)
        print(json.dumps(data, indent=4))
        print()
        # for repo in data["data"]["viewer"]["repositories"]["nodes"]:
        #     if repo["releases"]["totalCount"] and repo["name"] not in repo_names:
        #         repos.append(repo)
        #         repo_names.add(repo["name"])
        #         releases.append(
        #             {
        #                 "repo": repo["name"],
        #                 "repo_url": repo["url"],
        #                 "description": repo["description"],
        #                 "release": repo["releases"]["nodes"][0]["name"]
        #                 .replace(repo["name"], "")
        #                 .strip(),
        #                 "published_at": repo["releases"]["nodes"][0]["publishedAt"],
        #                 "published_day": repo["releases"]["nodes"][0][
        #                     "publishedAt"
        #                 ].split("T")[0],
        #                 "url": repo["releases"]["nodes"][0]["url"],
        #             }
        #         )
        has_next_page = data["data"]["repository"]["issues"]["pageInfo"]["hasNextPage"]
        after_cursor = data["data"]["repository"]["issues"]["pageInfo"]["endCursor"]
    return releases

if __name__ == '__main__':
    fetch_releases(TOKEN)
        
