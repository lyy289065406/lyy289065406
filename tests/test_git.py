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
                    "repositoriesContributedTo": {
                        "nodes": [{
                            "isFork": False,
                            "owner": {"login": "example-org"},
                            "name": "custom-default-branch",
                            "url": "https://github.com/example-org/custom-default-branch",
                            "description": "Uses develop instead of main",
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
        self.assertEqual(12, repos[0].commit_cnt)
        query = FakeGraphqlClient.queries[0]
        self.assertIn("defaultBranchRef", query)
        self.assertIn("repositoriesContributedTo", query)
        self.assertIn("contributionTypes: [COMMIT]", query)
        self.assertNotIn('object(expression:', query)


if __name__ == "__main__":
    unittest.main()
