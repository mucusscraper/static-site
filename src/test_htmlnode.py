import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType
from raw_to_text import split_nodes_delimiter

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("a","value to be availed")
        node2 = HTMLNode("a","value to be availed")
        node3 = HTMLNode("a", "This is a HTML node", props={"href": "https://www.google.com"})
        node4 = HTMLNode("a", "This is a HTML node", props={"href": "https://www.google2.com"})
        props1 = HTMLNode("a", "This is a HTML node", props={"href": "https://www.google.com","target": "_blank",}).props_to_html()
        props2 = HTMLNode("a", "This is a HTML node", props={"href": "https://www.google.com","target": "_blank",}).props_to_html()
        props3 = HTMLNode("a", "This is a HTML node", props={"href": "https://www.google.com","target": "_not_blank",}).props_to_html()
        self.assertEqual(node1, node2)
        self.assertNotEqual(node3,node4)
        self.assertEqual(props1,props2)
        self.assertNotEqual(props1,props3)
    def test_leaf_to_html_p(self):
        node5 = LeafNode("p", "Hello, world!")
        node6 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node5.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node6.to_html(),'<a href="https://www.google.com">Click me!</a>')
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_raw_to_text(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        list_of_nodes = [TextNode("This is text with a `code block` word", TextType.TEXT),TextNode("maybe this is a text with a `code block word`", TextType.TEXT), TextNode("This is text with a `italic` `block` word", TextType.TEXT)]
        new_nodes_2 = split_nodes_delimiter(list_of_nodes, "`", TextType.CODE)
        self.assertEqual(
            new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT),]
        )
        self.assertEqual(new_nodes_2,[TextNode("This is text with a ",TextType.TEXT),TextNode("code block",TextType.CODE), TextNode(" word",TextType.TEXT), TextNode("maybe this is a text with a ",TextType.TEXT), TextNode("code block word",TextType.CODE), TextNode("This is text with a ",TextType.TEXT), TextNode("italic",TextType.CODE),TextNode(" ",TextType.TEXT), TextNode("block",TextType.CODE), TextNode(" word",TextType.TEXT) ])
if __name__ == "__main__":
    unittest.main()
