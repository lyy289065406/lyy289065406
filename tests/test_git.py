#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch

from src.utils import _git


class FakeGraphqlClient:

    queries = []

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def exec(self, query, headers, proxy):
        self.queries.append(query)
        return {
            "data": {
                "viewer": {
                    "repositories": {
                        "nodes": [{
                            "isFork": False,
                            "owner": {"login": "example-org"},
                            "name": "custom-default-branch",
                            "url": "https://github.com/example-org/custom-default-branch",
                            "description": "Uses develop instead of main",
                            "visibility": "PUBLIC",
                            "pushedAt": "2026-07-02T08:00:00Z",
                            "repositoryTopics": {"nodes": []},
                            "defaultBranchRef": {
                                "target": {"history": {"totalCount": 12}}
                            },
                        }],
                        "pageInfo": {"hasNextPage": False, "endCursor": None},
                    }
                }
            }
        }


class QueryReposTest(unittest.TestCase):

    @patch.object(_git, "_GraphqlClient", FakeGraphqlClient)
    def test_includes_org_repo_with_custom_default_branch(self):
        FakeGraphqlClient.queries = []

        repos = _git.query_repos("token")

        self.assertEqual(1, len(repos))
        self.assertEqual("example-org", repos[0].owner)
        self.assertEqual("PUBLIC", repos[0].visibility)
        self.assertEqual(12, repos[0].commit_cnt)
        query = FakeGraphqlClient.queries[0]
        self.assertIn("defaultBranchRef", query)
        self.assertIn("repositories", query)
        self.assertIn("affiliations: [OWNER, COLLABORATOR, ORGANIZATION_MEMBER]", query)
        self.assertNotIn("repositoriesContributedTo", query)
        self.assertIn("visibility", query)
        self.assertNotIn('object(expression:', query)


    def test_paginates_and_skips_forks_and_empty_repositories(self):
        from copy import deepcopy
        first = FakeGraphqlClient("unused").exec("", {}, "")
        node = first["data"]["viewer"]["repositories"]["nodes"][0]
        fork = deepcopy(node)
        fork["isFork"] = True
        empty = deepcopy(node)
        empty["defaultBranchRef"] = None
        first["data"]["viewer"]["repositories"]["nodes"].extend([fork, empty])
        first["data"]["viewer"]["repositories"]["pageInfo"] = {
            "hasNextPage": True, "endCursor": "page-two"
        }
        second = deepcopy(first)
        second["data"]["viewer"]["repositories"]["nodes"] = [deepcopy(node)]
        second["data"]["viewer"]["repositories"]["nodes"][0]["name"] = "second-page"
        second["data"]["viewer"]["repositories"]["pageInfo"] = {
            "hasNextPage": False, "endCursor": None
        }
        with patch.object(_git, "_GraphqlClient") as client:
            client.return_value.exec.side_effect = [first, second]
            repos = _git.query_repos("token")
            self.assertEqual(["custom-default-branch", "second-page"], [r.name for r in repos])
            calls = client.return_value.exec.call_args_list
            self.assertIn("after: null", calls[0].kwargs["query"])
            self.assertIn('after: "page-two"', calls[1].kwargs["query"])


if __name__ == "__main__":
    unittest.main()
