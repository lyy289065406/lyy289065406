#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from src.bean.repo import Repo
from src.builder import activity


class ActivityTest(unittest.TestCase):

    def test_renders_public_and_non_public_visibility(self):
        repos = [
            Repo("owner", "public-repo", "https://example/public", "", "PUBLIC", "2026-07-02 00:00:00", 1),
            Repo("owner", "private-repo", "https://example/private", "", "PRIVATE", "2026-07-01 00:00:00", 1),
        ]

        table = activity.build(repos, top=2)

        self.assertIn("| repo | visibility | description |", table)
        self.assertIn("| 公开 |", table)
        self.assertIn("| 非公开 |", table)
        self.assertNotIn("\n\n| [", table)
        self.assertIn(
            "| 公开 |", table.splitlines()[3]
        )
        self.assertIn(
            "| 非公开 |", table.splitlines()[4]
        )


if __name__ == "__main__":
    unittest.main()
