from textnode import TextNode, TextType
import  os
import shutil
from extract_markdown import *

def copy_recursive(src,dst):
    if os.path.isfile(src):
        # dst_file = os.path.join(dst, os.path.basename(src))
        os.makedirs(os.path.dirname(dst),exist_ok=True)
        shutil.copy2(src,dst)
    else:
        os.makedirs(dst,exist_ok=True)
        for name in os.listdir(src):
            copy_recursive(
                os.path.join(src,name),
                os.path.join(dst,name),
            )
            # src_child = os.path.join(src,name)
            # dst_child = os.path.join(dst,name)
            # copy_recursive(src_child,dst_child)



def main():
    destination = "public"
    source = "static"
    shutil.rmtree(destination)
    os.mkdir(destination)
    copy_recursive(source,destination)
    for root, dirs, files in os.walk("content"):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root,file)
                rel = os.path.relpath(root,"content")
                dest_dir = os.path.join("public",rel)
                dest_path = os.path.join(dest_dir,file[:-3]+".html")
                generate_page(
                        from_path=full_path,
                        template_path="template.html",
                        dest_path=dest_path,
                )
        # if "index.md" in files:
            # full_path = os.path.join(root,"index.md")
            # rel = os.path.relpath(root,"content")
            # dest_dir = os.path.join("public",rel)
            # dest_path=os.path.join(dest_dir,"index.html")
            # generate_page(
                # from_path=full_path,
                # template_path="template.html",
                # dest_path=dest_path,
            # )
if __name__ == "__main__":
    main()

