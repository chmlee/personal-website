import os
import yaml
import sys
import markdown


# load config file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# find menu structure and template preference
config_dict = config["menu"]
menu_list = list(menu_dict.keys())

# check if directory exist in content
sub_dir = os.listdir('content')
for menu_item in menu_list:
    if menu_item not in sub_dir:
        sys.exit(print("Subdirectory", menu_item, "not found in Content directory"))

# loop to create pages

for menu_item in menu_list:


menu_item = "Home"
with open("content/" + menu_item + "/index.md", "r") as file: 
    md_file = file.read() 

content = markdown.markdown(md_file, extensions = ['meta', 'mdx_math'])

md = markdown.Markdown(extensions = ['meta', 'mdx_math'])
md.convert(md_file)
meta = md.Meta



env = jinja2.Environment(loader=jinja2.FileSystemLoader("template"))
main_template = env.get_template('main.html')   
html_output = main_template.render(menu_list = menu_list, content = content)

with open("static/" + menu_item + "/index.html", 'w') as file: 
    file.write(html_output) 

