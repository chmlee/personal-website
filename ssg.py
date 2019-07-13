import os
import yaml
import sys
import markdown
import jinja2
import shutil
import glob

# load config file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)



# find menu structure and template preference
config_menu = config["menu"]



# check if content exist
content_list = os.listdir('content')
support_format = ["md"]
file_not_found = []
content_ext_dict = {}
for config_menu_item in config_menu:
    for ext in support_format:
        content_name = config_menu_item + "." + ext
        if content_name in content_list:
            content_ext_dict[config_menu_item] = ext
            continue
        missing_file = "content/" + config_menu_item + ".md"
        #with open(missing_file, "w") as file:
        #    file.write("")
        file_not_found.append(config_menu_item)
if len(file_not_found) != 0:      #missing content, exit program
    print("Missing the following content:")
    for item in file_not_found:
        print("-", item)



# backup all existing html files
if "backup" in os.listdir():
    shutil.rmtree('backup')
os.mkdir('backup')
for item in os.listdir('static'):
    before = "static/" + item
    after = "backup/" + item
    os.rename(before, after)

# loop to create pages
loader = jinja2.FileSystemLoader(["module", "template"])
env = jinja2.Environment(loader = loader)
for menu_item in config_menu:
    if menu_item in file_not_found:
        content = ""
    else:
        content_dir = "content/" + menu_item + "." + content_ext_dict[menu_item]
        with open(content_dir, "r") as file: 
            md_file = file.read() 
        #extract content
        content = markdown.markdown(md_file, extensions = ['meta', 'mdx_math'])
        # extract meta data
        md = markdown.Markdown(extensions = ['meta', 'mdx_math'])
        md.convert(md_file)
        meta = md.Meta
    # choose template 
    config_template = config_menu[menu_item] + ".html"
    template = env.get_template(config_template)   
    html_output = template.render(
            menu_list = config_menu, 
            content = content
    )
    with open("static/" + menu_item + ".html", 'w') as file: 
        file.write(html_output) 

