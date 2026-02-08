from webpage import generate_page
import os

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    
    for d in os.listdir(dir_path_content):
        if os.path.isfile(os.path.join(dir_path_content, d)):
            if d.endswith(".md"):
                os.makedirs(dest_dir_path, exist_ok=True)
                generate_page(os.path.join(dir_path_content, d), template_path, f"{dest_dir_path}/{d.replace('.md', '.html')}")
        else:
            generate_pages_recursive(os.path.join(dir_path_content, d), template_path, os.path.join(dest_dir_path, d))
        
    