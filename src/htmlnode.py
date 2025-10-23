from textnode import TextNode, TextType
from enum import Enum

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError("This method is not implemented")
    def props_to_html(self):
        list_of_values = []
        for key in self.props:
            list_of_values.append(" ")
            list_of_values.append(key+"=")
            phrase_value = '"'+str(self.props[key]) +'"'
            list_of_values.append(phrase_value)
        phrase = ""
        for value in list_of_values:
            phrase = phrase + str(value)
        return phrase
    def __eq__(self,node2):
        if self.tag == node2.tag and self.value == node2.value and self.children == node2.children and self.props == node2.props:
            return True
        return False
    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        super().__init__(tag,value,None,props)
    def to_html(self):
        if self.value == None:
            raise ValueError("Value error")
        elif self.tag == None:
            return f"{self.value}"
        elif self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag,None,children,props)
    def to_html(self):
        if self.tag == None:
            raise ValueError("Value error")
        if self.children == None:
            raise ValueError("Missing children")
        else:
            new_phrase = ""
            for children in self.children:
                new_phrase = new_phrase + children.to_html()
            return f"<{self.tag}>{new_phrase}</{self.tag}>"

def text_node_to_html_node(text_node):
    if type(text_node) is TextNode:
        if text_node.text_type not in TextType:
            raise Exception("Exception")
        else:
            if text_node.text_type == TextType.TEXT:
                return LeafNode(tag=None, value=text_node.text)
            elif text_node.text_type == TextType.BOLD:
                return LeafNode(tag="b",value=text_node.text)
            elif text_node.text_type == TextType.ITALIC:
                return LeafNode(tag="i", value=text_node.text)
            elif text_node.text_type == TextType.CODE:
                return LeafNode(tag="code",value=text_node.text)
            elif text_node.text_type == TextType.LINK:
                return LeafNode(tag="a",value=text_node.text,props={"href": text_node.url})
            elif text_node.text_type == TextType.IMAGE:
                return LeafNode(tag="img",value= "",props={"src":text_node.url,"alt":text_node.text})
