import re
from textnode import TextNode, TextType
from htmlnode import LeafNode

from enum import Enum

class MarkdownType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    heading_match = re.match(r"^# (.*)$", block)
    if heading_match:
        return MarkdownType.HEADING
    elif block.startswith("```"):
        return MarkdownType.CODE
    elif block.startswith(">"):
        return MarkdownType.QUOTE
    elif block.startswith("-"):
        return MarkdownType.UNORDERED_LIST
    elif block.startswith("1."):
        return MarkdownType.ORDERED_LIST
    else:
        return MarkdownType.PARAGRAPH
    
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text_type == TextType.TEXT:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise ValueError("Invalid markdown, missing closing delimiter")
            for nsp in range(len(split_text)):
                if nsp % 2 == 0:
                    new_nodes.append(TextNode(split_text[nsp], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_text[nsp], text_type))
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text_to_process = node.text
        while True:
            matches = extract_markdown_images(text_to_process)
            if len(matches) == 0:
                if text_to_process != "":
                    new_nodes.append(TextNode(text_to_process, TextType.TEXT))
                break
            alt, url = matches[0]
            sections = text_to_process.split(f"![{alt}]({url})", 1)
            before = sections[0]
            after = sections[1]
            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text_to_process = after

        
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text_to_process = node.text
        while True:
            matches = extract_markdown_links(text_to_process)
            if len(matches) == 0:
                if text_to_process != "":
                    new_nodes.append(TextNode(text_to_process, TextType.TEXT))
                break
            alt, url = matches[0]
            sections = text_to_process.split(f"[{alt}]({url})", 1)
            before = sections[0]
            after = sections[1]
            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, url))
            text_to_process = after

        
    return new_nodes

def text_to_textnodes(text):
    # text to textnodes
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)

    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    block_md = []
    for block in blocks:
        block_md.append(block.strip())
    return block_md

from textnode import text_node_to_html_node 

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children


from htmlnode import ParentNode
import re


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent = ParentNode("div", [])
    for block in blocks:
        if not block.strip():
            continue
        block_type = block_to_block_type(block)
        if block_type == MarkdownType.PARAGRAPH:
            block = block.strip("\n ").strip()
            block = " ".join(block.split())
            children = text_to_children(block)
            p_node = ParentNode("p", children)
            parent.children.append(p_node)

        elif block_type == MarkdownType.HEADING:
            match = re.match(r"^(#+) (.*)$", block)
            children = text_to_children(match.group(2))
            h_node = ParentNode(f"h{len(match.group(1))}", children)
            parent.children.append(h_node)

        elif block_type == MarkdownType.CODE:
            lines = block.split("\n")
            block = "\n".join(lines[1:-1]) + "\n"
            text_node = TextNode(block, TextType.TEXT)
            html_node = text_node_to_html_node(text_node)
            code_node = ParentNode("code", [html_node])
            parent_html = ParentNode("pre", [code_node])
            parent.children.append(parent_html)

        elif block_type == MarkdownType.QUOTE:
            block = block.split("\n")
            bl_clean = []
            for bl in block:
                bl = bl.strip(">").strip()
                bl_clean.append(bl)
            combined = " ".join(bl_clean)
            children = text_to_children(combined)
            
            quote_node = ParentNode("blockquote", children)
            parent.children.append(quote_node)

        elif block_type == MarkdownType.UNORDERED_LIST:
            block = block.split("\n")
            ul_list = []
            for child in block:
                old_child = child.strip("*-").strip()
                children = text_to_children(old_child)
                li_node = ParentNode("li", children)
                ul_list.append(li_node)
            ul_node = ParentNode("ul", ul_list)
            parent.children.append(ul_node)


        elif block_type == MarkdownType.ORDERED_LIST:
            block = block.split("\n")
            ol_list = []
            for child in block:
                # Find where ". " appears and take everything after it
                old_child = re.sub(r'^\d+\.\s*', '', child)
                children = text_to_children(old_child)
                li_node = ParentNode("li", children)
                ol_list.append(li_node)
            ol_node = ParentNode("ol", ol_list)
            parent.children.append(ol_node)
    return parent
    
def markdown_to_html(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == MarkdownType.PARAGRAPH:
            TextNode(block, TextType.TEXT)
        elif block_type == MarkdownType.HEADING:
            TextNode(block, TextType.HEADING)
        elif block_type == MarkdownType.CODE:
            TextNode(block, TextType.CODE)
        elif block_type == MarkdownType.QUOTE:
            TextNode(block, TextType.QUOTE)
        elif block_type == MarkdownType.UNORDERED_LIST:
            TextNode(block, TextType.UNORDERED_LIST)
        elif block_type == MarkdownType.ORDERED_LIST:
            TextNode(block, TextType.ORDERED_LIST)


