import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_link(self):
        node1 = TextNode("boot.dev", TextType.LINK)
        node2 = TextNode("boot.dev", TextType.LINK)
        self.assertEqual(node1, node2)
    def test_italic_bold(self):
        node = TextNode("This is italic", TextType.ITALIC)
        node2 = TextNode("This is italic", TextType.BOLD)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
