import unittest

from block_markdown import markdown_to_blocks, BlockType, block_to_block_type, text_to_children, markdown_to_html_node 
class TestBlockMarkdown(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )
        def test_block_type(self):
            phrase1 = "### Hello coleagues"
            phrase2 = "```Testing a code block```"
            phrase3 = ">Quoting"
            phrase4 = "- Unoredered Lists"
            phrase5 = "39. Ordered Lists"
            phrase6 = "Normal paragraph"
            phrase7 = "# 39. Headings"
            phrase_1_result = block_to_block_type(phrase1)
            phrase_2_result = block_to_block_type(phrase2)
            phrase_3_result = block_to_block_type(phrase3)
            phrase_4_result = block_to_block_type(phrase4)
            phrase_5_result = block_to_block_type(phrase5)
            phrase_6_result = block_to_block_type(phrase6)
            phrase_7_result = block_to_block_type(phrase7)
            self.assertEqual(phrase_1_result,BlockType.HEADING)
            self.assertEqual(phrase_2_result,BlockType.CODE)
            self.assertEqual(phrase_3_result,BlockType.QUOTE)
            self.assertEqual(phrase_4_result,BlockType.UNORDERED_LIST)
            self.assertEqual(phrase_5_result,BlockType.ORDERED_LIST)
            self.assertEqual(phrase_6_result,BlockType.PARAGRAPH)
            self.assertEqual(phrase_7_result,BlockType.HEADING)
        def test_paragraphs(self):
            md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            )

        def test_codeblock(self):
            md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            )
if __name__ == "__main__":
    unittest.main()
