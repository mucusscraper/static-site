import os
from textnode import *
from htmlnode import *
from raw_to_text import *
from regex_patterns import *
from block_markdown import *


def extract_title(markdown_file):
    # markdown_file = open(markdown,'r')
    for line in markdown_file.splitlines():
        s = line.lstrip()
        if s.startswith("# ") and not s.startswith("##"):
            return s[2:].strip()
    raise Exception("No header")

def generate_page(from_path,template_path,dest_path,basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path,'r') as f:
        md = f.read()
    with open(template_path,'r') as f:
        template = f.read()
    html_content = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    page2 = page.replace('href="/',f'href="{basepath}').replace('src="/',f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page2)
