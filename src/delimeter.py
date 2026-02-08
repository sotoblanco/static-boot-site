from textnode import TextNode, TextType

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


