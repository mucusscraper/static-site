from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	list_of_new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			list_of_new_nodes.append(node)
		else:
			separated_texts = node.text.split(delimiter)
			if len(separated_texts) == 1:
				list_of_new_nodes.append(node)
			else:
				for i, separated_text in enumerate(separated_texts):
					if separated_text == "":
						continue
					if i%2 == 0:
						new_node = TextNode(separated_text, TextType.TEXT)
					else:
						new_node = TextNode(separated_text, text_type)
					list_of_new_nodes.append(new_node)
	return list_of_new_nodes
