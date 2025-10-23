from textnode import TextNode, TextType
import  os
import shutil
from extract_markdown import *
import sys

def copy_recursive(src,dst):
    if os.path.isfile(src):
        os.makedirs(os.path.dirname(dst),exist_ok=True)
        shutil.copy2(src,dst)
    else:
        os.makedirs(dst,exist_ok=True)
        for name in os.listdir(src):
            copy_recursive(
                os.path.join(src,name),
                os.path.join(dst,name),
            )
def main():
    if len(sys.argv) == 1:
        basepath = "/"
    elif len(sys.argv) == 2:
        basepath = sys.argv[1]
    else:
        raise Exception("Error with number of arguments")
    destination = "docs"
    source = "static"
    shutil.rmtree(destination)
    os.mkdir(destination)
    copy_recursive(source,destination)
    for root, dirs, files in os.walk("content"):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root,file)
                rel = os.path.relpath(root,"content")
                dest_dir = os.path.join(destination,rel)
                dest_path = os.path.join(dest_dir,file[:-3]+".html")
                generate_page(
                        from_path=full_path,
                        template_path="template.html",
                        dest_path=dest_path,
                        basepath=basepath
                )

if __name__ == "__main__":
    main()

