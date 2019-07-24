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

# load default config from theme if not customized
config_theme = config['Theme']
with open('theme/' + config_theme + '/config.yaml') as f:
    default_config = yaml.safe_load(f)
for config_menu_item in config['Menu']:
    template = config['Menu'][config_menu_item]
    if config_menu_item not in config:
        config[config_menu_item] = default_config[template]
    else:
        for cls in default_config[template]:
            if cls not in config[config_menu_item]:
                config[config_menu_item][cls] = default_config[template][cls]

# search for content file
content_listdir = os.listdir('content')
support_format = ["md"]
file_not_found = []
content_file_dict = {}
for config_menu_item in config['Menu']:
    for ext in support_format:
        content_file_name = config_menu_item + "." + ext
        if content_file_name in content_listdir:
            content_file_dict[config_menu_item] = content_file_name
            break


# backup everything in static
if ".backup" in os.listdir():
    shutil.rmtree('.backup')
os.mkdir('.backup')
if "static" not in os.listdir():
    os.mkdir('static')
for item in os.listdir('static'):
    before = "static/" + item
    after = ".backup/" + item
    os.rename(before, after)

# loop to create pages

# read template
loader = jinja2.FileSystemLoader(["theme", "module"])
env = jinja2.Environment(loader = loader)
for config_menu_item in config['Menu']:
    # read content file if exist
    try:
        content_file_name = content_file_dict[config_menu_item]
        content_file_ext = content_file_name.split('.')[-1:]
        content_dir = "content/" + content_file_name 
        with open(content_dir, "r") as file: 
            content_file = file.read() 
        # parse content to html
        # md -> html
        if ext == 'md':
            md = markdown.Markdown(extensions = ['meta', 'mdx_math'])
            content = md.convert(content_file)
            meta = md.Meta
    except KeyError:
        content = None
        meta = None

    # choose template 
    config_template = config['Menu'][config_menu_item] + ".html"
    template = env.get_template(config['Theme'] + '/' + config_template)   
    html_output = template.render(
            config = config,
            config_menu_item = config_menu_item,
            content = content
    )

    # write html
    with open("static/" + config_menu_item + ".html", 'w') as f: 
        f.write(html_output) 
    # create index.html
    if config_menu_item == "Home":
        html_output = html_output.replace('css/', 'static/css/')
        html_output = html_output.replace('../custom', 'custom/')
        with open("index.html", 'w') as f: 
            f.write(html_output)



# css

# copy style.css and <template>.cssfrom theme to static
os.mkdir('static/css')
d0 = 'theme/' + config['Theme'] + '/css/'
d1 = 'static/css/'
before = d0 + 'style.css'
after = d1 + 'style.css'
shutil.copyfile(before, after)
for menu_item in config['Menu']:
    template = config['Menu'][menu_item]
    after = d1 + template + '.css'
    if os.path.isfile(after) == False:
        before = d0 + template + '.css'
        shutil.copyfile(before, after)



# generate mod.css
# find all mod used
mod_list = [] 
for menu_item in config['Menu']: 
    menu_item_dict = config[menu_item] 
    for key in menu_item_dict: 
        for mod in menu_item_dict[key]: 
            if mod not in mod_list: 
                mod_list.append(mod) 

# find individual <mod>.css
with open('static/css/mod.css', 'w') as f:
    for mod in mod_list:
        # locate which css to load for each mod
        target = 'custom/css/' + mod + '.css'
        if os.path.isfile(target):
            mod_css = target
        else:
            target  = 'theme/' + config_theme + '/css/' + mod + '.css'
            if os.path.isfile(target):
                mod_css = target
            else:
                target = 'module/' + mod +'style.css'
                if os.path.isfile(target):
                    mod_css = target
                else: mod_css = None
        # copy <mod>.css into mod.css
        if mod_css != None:
            with open(mod_css) as css_file:
                f.writelines(css_file)


