from webpage import extract_title


import unittest

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Title\n## Subtitle\n### Sub-subtitle"
        self.assertEqual(extract_title(markdown), "Title")

if __name__ == "__main__":
    unittest.main()