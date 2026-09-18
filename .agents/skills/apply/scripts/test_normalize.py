#!/usr/bin/env python3
"""
Comprehensive regression test suite for text normalization.
Covers:
1. Empty and whitespace-only inputs
2. Single-paragraph line unwrapping
3. Multi-paragraph preservation (preserving \n\n boundaries)
4. Protection against false bullets: words starting with 'o' ('of', 'on', 'our')
5. Protection against false bullets: negative numbers and hyphens ('-15%')
6. Protection against false bullets: markdown italics ('*important*')
7. Support for large circle glyph '⬤' (\u2b24) from user's screenshot without spaces
8. Standard Unicode bullet glyphs (⚫, ●, ▪, ◆, etc.)
9. Trailing hyphen line break rejoining ('inter-\nrater' -> 'inter-rater')
10. Missing space correction after commas, colons, and periods ('MCP,programmatically', 'Skills:Python', 'QA.Iterative')
11. User's exact case from TikTok application
"""

import sys
import unittest

from text_normalizer import normalize_text

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class TestTextNormalization(unittest.TestCase):
    def test_01_empty_and_whitespace(self):
        self.assertEqual(normalize_text(""), "")
        self.assertEqual(normalize_text("   \n\n  \t  "), "")

    def test_02_paragraph_unwrapping(self):
        bio = "I am an undergraduate student at UCL\nstudying Psychology and Language\nSciences."
        expected_bio = "I am an undergraduate student at UCL studying Psychology and Language Sciences."
        self.assertEqual(normalize_text(bio), expected_bio)

    def test_03_multi_paragraph_preservation(self):
        p2 = "Para 1 line 1\nline 2.\n\nPara 2 line 1\nline 2."
        expected_p2 = "Para 1 line 1 line 2.\n\nPara 2 line 1 line 2."
        self.assertEqual(normalize_text(p2), expected_p2)

    def test_04_words_starting_with_o_preserved(self):
        text_with_o = "Engineered data pipeline\nof 500k records\non AWS cloud platform\nfor our core team."
        expected_o = "Engineered data pipeline of 500k records on AWS cloud platform for our core team."
        self.assertEqual(normalize_text(text_with_o), expected_o)

    def test_05_negative_numbers_and_hyphens_preserved(self):
        neg_text = "• Reduced model latency by\n-15% across endpoints\nthrough batching."
        expected_neg = "• Reduced model latency by -15% across endpoints through batching."
        self.assertEqual(normalize_text(neg_text), expected_neg)

    def test_06_markdown_italics_preserved(self):
        italics_text = "Employed\n*iterative* testing."
        expected_italics = "Employed *iterative* testing."
        self.assertEqual(normalize_text(italics_text), expected_italics)

    def test_07_large_circle_glyph_handled(self):
        large_circle_text = "⬤Engineered an LLM classification pipeline.\n⬤Automated data collection."
        expected_large_circle = "• Engineered an LLM classification pipeline.\n• Automated data collection."
        self.assertEqual(normalize_text(large_circle_text), expected_large_circle)

    def test_08_standard_unicode_bullets_standardized(self):
        raw_bullets = (
            "⚫Engineered something.\n●Built pipeline.\n▪Analyzed data.\n◆Tested models.\no Handled interviews."
        )
        expected_raw_bullets = (
            "• Engineered something.\n• Built pipeline.\n• Analyzed data.\n• Tested models.\n• Handled interviews."
        )
        self.assertEqual(normalize_text(raw_bullets), expected_raw_bullets)

    def test_09_trailing_hyphen_rejoined(self):
        hyphen_text = "• Achieving high inter-\nrater reliability and high-\nperformance data loaders."
        expected_hyphen = "• Achieving high inter-rater reliability and high-performance data loaders."
        self.assertEqual(normalize_text(hyphen_text), expected_hyphen)

    def test_10_missing_space_after_punctuation(self):
        punct_text = "• Core competencies:Python,SQL,Docker.Conducted 10+ sprints."
        expected_punct = "• Core competencies: Python, SQL, Docker. Conducted 10+ sprints."
        self.assertEqual(normalize_text(punct_text), expected_punct)

    def test_11_user_tiktok_case(self):
        user_case = (
            "●Engineered an LLM classification pipeline to evaluate 700+ papers against screening criteria, achieving high\n"
            "inter-rater reliability (κ = 0.98) while resolving complex edge cases through iterative QA refinement.\n"
            "● Automated the collection and deduplication of 600+ papers by linking journal APIs to Zotero via MCP,\n"
            "programmatically archiving citation metadata and full-text PDFs."
        )
        expected_user = (
            "• Engineered an LLM classification pipeline to evaluate 700+ papers against screening criteria, achieving high inter-rater reliability (κ = 0.98) while resolving complex edge cases through iterative QA refinement.\n"
            "• Automated the collection and deduplication of 600+ papers by linking journal APIs to Zotero via MCP, programmatically archiving citation metadata and full-text PDFs."
        )
        self.assertEqual(normalize_text(user_case), expected_user)

    def test_12_email_address_protected_from_dot_space_injection(self):
        email_text = "Contact candidate at Kyubin.Yun@ucl.ac.uk or test.user@example.com for inquiries."
        expected = "Contact candidate at Kyubin.Yun@ucl.ac.uk or test.user@example.com for inquiries."
        self.assertEqual(normalize_text(email_text), expected)

    def test_13_url_protected_from_punctuation_clean(self):
        url_text = "View application at https://job-boards.greenhouse.io/scaleai/jobs/4730846005 for details."
        expected = "View application at https://job-boards.greenhouse.io/scaleai/jobs/4730846005 for details."
        self.assertEqual(normalize_text(url_text), expected)

    def test_14_nbsp_normalized_to_ascii_space(self):
        nbsp_text = "Kyubin\u00a0Yun\u00a0London\u00a0NW2\u00a08BB"
        expected = "Kyubin Yun London NW2 8BB"
        self.assertEqual(normalize_text(nbsp_text), expected)
        self.assertNotIn("\u00a0", normalize_text(nbsp_text))


def test_normalization():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTextNormalization)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        raise AssertionError("Text normalization regression tests failed!")
    print("All text normalization regression tests passed successfully!")


if __name__ == "__main__":
    test_normalization()
