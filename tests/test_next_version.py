import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from next_version import next_tag


class NextTagTests(unittest.TestCase):
    def test_feat_bumps_minor(self):
        self.assertEqual(next_tag("v1.2.3", ["feat: add x"]), "v1.3.0")

    def test_fix_bumps_patch(self):
        self.assertEqual(next_tag("v1.2.3", ["fix: y"]), "v1.2.4")

    def test_breaking_bumps_major(self):
        self.assertEqual(next_tag("v1.2.3", ["feat!: remove z"]), "v2.0.0")
        self.assertEqual(next_tag("v1.2.3", ["fix: q\n\nBREAKING CHANGE: api"]), "v2.0.0")

    def test_highest_wins(self):
        self.assertEqual(next_tag("v1.2.3", ["fix: a", "feat: b", "docs: c"]), "v1.3.0")

    def test_docs_only_means_no_release(self):
        self.assertIsNone(next_tag("v1.2.3", ["docs: a", "chore: b", "Initial commit"]))

    def test_first_release_from_nothing(self):
        self.assertEqual(next_tag(None, ["feat: first"]), "v0.1.0")

    def test_scope_is_allowed(self):
        self.assertEqual(next_tag("v0.1.0", ["fix(api): y"]), "v0.1.1")


if __name__ == "__main__":
    unittest.main()
