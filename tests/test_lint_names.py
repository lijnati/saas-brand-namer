import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "saas-brand-namer" / "scripts"))
from lint_names import lint  # noqa: E402


def status(name):
    return lint(name)[1]


class RealBrandsPass(unittest.TestCase):
    """One-word brands we want the skill to produce must not be rejected."""

    def test_known_good_names(self):
        for name in [
            "Vercel", "Figma", "Twilio", "Zapier", "Attio", "Granola", "Kodak",
            "Resend", "Linear", "Notion", "Stripe", "Ramp", "Loom", "Clerk",
            "Plaid", "Gusto", "Zed", "Arc", "Cursor", "Sentry", "Asana", "Carpet",
        ]:
            with self.subTest(name=name):
                self.assertEqual(status(name), "PASS")

    def test_real_words_with_l_or_r_clusters_pass(self):
        for name in ["Settle", "Raffle", "Ripple", "Kindling", "Lanyard", "Strength"]:
            with self.subTest(name=name):
                self.assertNotEqual(status(name), "FAIL")


class SlopFails(unittest.TestCase):
    def test_camelcase_compounds(self):
        for name in ["ScopePilot", "BriefBridge", "VendorVault", "CostGuard", "TokenGuard"]:
            with self.subTest(name=name):
                self.assertEqual(status(name), "FAIL")

    def test_lowercase_glued_compounds(self):
        for name in ["Scopepilot", "Briefbridge", "Costwise", "Sunpath", "Matchbox", "Flowhub"]:
            with self.subTest(name=name):
                self.assertEqual(status(name), "FAIL")

    def test_stuck_on_suffixes(self):
        for name in ["Taskly", "Budgetio", "Spendify", "Ledgerly", "Zenai", "Omnisync"]:
            with self.subTest(name=name):
                self.assertEqual(status(name), "FAIL")

    def test_single_word_cliches(self):
        for name in ["Nexus", "Lumina", "Aegis", "Sentinel", "Vertex", "Pulse"]:
            with self.subTest(name=name):
                self.assertEqual(status(name), "FAIL")

    def test_not_a_single_token(self):
        for name in ["Cost Guard", "Spend-wise", "Name2", "get.name"]:
            with self.subTest(name=name):
                self.assertEqual(status(name), "FAIL")

    def test_unpronounceable(self):
        self.assertEqual(status("Brdgx"), "FAIL")


class Warnings(unittest.TestCase):
    def test_vowel_dropped(self):
        self.assertEqual(status("Tumblr"), "WARN")

    def test_compound_dictionary_word_warns(self):
        self.assertEqual(status("Dropbox"), "WARN")


if __name__ == "__main__":
    unittest.main()
