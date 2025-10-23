from enum import Enum
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from raw_to_text import split_nodes_delimiter
from regex_patterns import *

def markdown_to_blocks(markdown):
    divided_blocks = markdown.split("\n\n")
    list_with_stripped_divided_blocks = []
    for element in divided_blocks:
        if len(element) != 0:
            list_with_stripped_divided_blocks.append(element.strip())
    return list_with_stripped_divided_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST =  "unordered_list"
    ORDERED_LIST = "ordered_list"
    
def block_to_block_type(block_of_markdown_text):
    if block_of_markdown_text.startswith("```") and block_of_markdown_text.endswith("```"):
        return BlockType.CODE
    lines = block_of_markdown_text.splitlines()
    first_line_stripped = lines[0].lstrip()
    n = len(first_line_stripped) - len(first_line_stripped.lstrip("#"))
    if 1 <= n <= 6 and first_line_stripped[n:].startswith(" "): 
        return BlockType.HEADING
    if all(l.startswith(">") for l in lines):
        return BlockType.QUOTE
    if all(l.startswith("- ") for l in lines):
        return BlockType.UNORDERED_LIST
    def is_ol_line(l: str) -> bool:
        head, sep, tail = l.partition(". ")
        return sep == ". " and head.isdigit()
    if all(is_ol_line(l) for l in lines):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_to_children(markdown_block):
    textnodes = text_to_textnodes(markdown_block)
    list_of_html_nodes = []
    for textnode in textnodes:
        htmlnode = text_node_to_html_node(textnode)
        list_of_html_nodes.append(htmlnode)
    return list_of_html_nodes

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    full_list_of_htmls = []
    for markdown_block in markdown_blocks:
        block_type = block_to_block_type(markdown_block)
        list_of_children = text_to_children(markdown_block)
        if block_type == BlockType.PARAGRAPH:
            modified_markdown_block = markdown_block.replace("\n", " ")
            list_of_children = text_to_children(modified_markdown_block)
            parent_node = ParentNode("p",list_of_children)
            full_list_of_htmls.append(parent_node)
        elif block_type == BlockType.QUOTE:
            lines = []
            for l in markdown_block.splitlines():
                s = l.lstrip()
                if s.startswith(">"):
                    s = s[1:].lstrip()
                lines.append(s)
            text = " ".join(lines)
            children = text_to_children(text)
            parent_node = ParentNode("blockquote", children)
            full_list_of_htmls.append(parent_node)
        elif block_type == BlockType.UNORDERED_LIST:
            items = []
            for line in markdown_block.splitlines():
                s = line.lstrip()
                if not s or not s.startswith("- "):
                    continue
                items.append(s[2:])
            full_list_of_htmls.append(
                ParentNode("ul", [ParentNode("li", text_to_children(it)) for it in items])
            )
        elif block_type == BlockType.ORDERED_LIST:
            items = []
            def is_ol_line(l: str) -> bool:
                head, sep, tail = l.partition(". ")
                return sep == ". " and head.isdigit()
            for line in markdown_block.splitlines():
                s = line.lstrip()
                if is_ol_line(s):
                    items.append(s[3:])
            full_list_of_htmls.append(
                ParentNode("ol", [ParentNode("li", text_to_children(it)) for it in items])
            )
        elif block_type == BlockType.HEADING:
            first = markdown_block.splitlines()[0].lstrip()
            n = len(first) - len(first.lstrip("#"))
            text = first[n:].lstrip()
            children = text_to_children(text)
            parent_node = ParentNode(f"h{n}", children)
            full_list_of_htmls.append(parent_node)
        elif block_type == BlockType.CODE:
            lines = markdown_block.splitlines()
            inner = "\n".join(lines[1:-1])
            parent_node = ParentNode("pre", [LeafNode("code", inner)])
            full_list_of_htmls.append(parent_node)
    full_parent_node = ParentNode("div",full_list_of_htmls)
    return full_parent_node

