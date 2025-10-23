import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        node4 = TextNode("This is a text node", TextType.ITALIC)
        node5 = TextNode("This is a text node", TextType.LINK, "google.com")
        node6 = TextNode("This is a text node", TextType.LINK, "google.com")
        node7 = TextNode("This is a text node", TextType.LINK, "google.com")
        node8 = TextNode("This is a text node", TextType.LINK, "google2.com")
        node10 = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node, node2)
        self.assertEqual(node3,node4)
        self.assertEqual(node5,node6)
        self.assertNotEqual(node7,node8)
        self.assertNotEqual(node7,node10)

if __name__ == "__main__":
    unittest.main()
