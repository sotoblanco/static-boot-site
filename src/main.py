
from textnode import TextNode
from webpage import generate_page
from generate_page_rec import generate_pages_recursive

def move_sources(source_dir, dest_folder, is_root=True):
    import os
    import shutil
    # list the source folder
    dir = os.listdir(source_dir)
    # iterate over dir to get the files
    if is_root:
        if os.path.exists(dest_folder):
            shutil.rmtree(dest_folder)
    os.mkdir(dest_folder)
    for d in dir:
        source_path = os.path.join(source_dir, d)
        dest_path = os.path.join(dest_folder, d)
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        else:
            move_sources(source_path, dest_path, is_root=False)


def main():
    import sys
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    node = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    print(node)
    move_sources("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)
if __name__ == "__main__":
    main()

