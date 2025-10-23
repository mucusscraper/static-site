import re
from textnode import TextNode, TextType
from raw_to_text import split_nodes_delimiter

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)]\((.*?)\)",text)
    list_of_tuples = []
    for match in matches:
        list_of_tuples.append((match[0],match[1]))
    return list_of_tuples


def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)]\((.*?)\)",text)
    list_of_tuples = []
    for match in matches:
        list_of_tuples.append((match[0],match[1]))
    return list_of_tuples

def split_nodes_link(old_nodes):
    list_of_new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            list_of_new_nodes.append(node)
        else:
            get_links = extract_markdown_links(node.text)
            if len(get_links) == 0:
                list_of_new_nodes.append(node)
            else:
                cursor = 0
                for text,url in get_links:
                    md = f"[{text}]({url})"
                    start = node.text.find(md,cursor)
                    if start == -1:
                        break
                    if start > cursor:
                        list_of_new_nodes.append(TextNode(node.text[cursor:start], TextType.TEXT))
                    list_of_new_nodes.append(TextNode(text, TextType.LINK, url))
                    cursor = start + len(md)
                if cursor < len(node.text):
                    list_of_new_nodes.append(TextNode(node.text[cursor:], TextType.TEXT))
    return list_of_new_nodes

def split_nodes_image(old_nodes):
    list_of_new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            list_of_new_nodes.append(node)
        else:
            get_images = extract_markdown_images(node.text)
            if len(get_images) == 0:
                list_of_new_nodes.append(node)
            else:
                cursor = 0
                for text,image_link in get_images:
                    md = f"![{text}]({image_link})"
                    start = node.text.find(md,cursor)
                    if start == -1:
                        break
                    if start > cursor:
                        list_of_new_nodes.append(TextNode(node.text[cursor:start], TextType.TEXT))
                    list_of_new_nodes.append(TextNode(text, TextType.IMAGE, image_link))
                    cursor = start + len(md)
                if cursor < len(node.text):
                    list_of_new_nodes.append(TextNode(node.text[cursor:], TextType.TEXT))
    return list_of_new_nodes

def text_to_textnodes(text):
    list_of_nodes = [TextNode(text, TextType.TEXT)]
    list_of_nodes = split_nodes_delimiter(list_of_nodes,'`',TextType.CODE)
    list_of_nodes = split_nodes_delimiter(list_of_nodes,'**',TextType.BOLD)
    list_of_nodes = split_nodes_delimiter(list_of_nodes,'_',TextType.ITALIC)
    list_of_nodes = split_nodes_image(list_of_nodes)
    list_of_nodes = split_nodes_link(list_of_nodes)
    return list_of_nodes
