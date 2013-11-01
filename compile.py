#!/usr/bin/env python

import iso8601
import json
import os
import shutil

from jinja2 import Environment, FileSystemLoader

## Start configuration options ##
# directory where to start looking for templates
content_dir = os.path.join(os.getcwd(), 'content')
# directory where to save generated files
output_dir = os.path.join(os.getcwd(), 'output')
# directory where templates are stored
template_dir = os.path.join(os.getcwd(), 'templates')
# source content files suffix
content_ext = '.json'

## End configuration options ##

def get_content_list():
    content_files = ((f, os.path.join(content_dir, f)) for f in os.listdir(content_dir) if f.endswith(content_ext))

    content_list = []

    for f, fpath in content_files:
        #print "Now file:", f
        fname, ext = os.path.splitext(f)

        context = json.loads(open(fpath).read())

        context["date"] = iso8601.parse_date(context["date"])
        context["name"] = fname
        context["slug"] = "/%s/" % (fname,)

        content_list.append(context)

    content_list.sort(key=lambda c: c["date"])

    for idx, context in enumerate(content_list):
        context["prev_slug"] = content_list[idx - 1]["slug"] if idx > 0 else None
        context["next_slug"] = content_list[idx + 1]["slug"] if idx < len(content_list) - 1 else None

    return content_list


def gen_html_pages(content_list, jinja_env):

    template = jinja_env.get_template("index.jnj")

    for context in content_list:
        #print "Now name:", context["name"], context["date"]

        o = template.render(context)

        dest_dir = os.path.join(output_dir, context["name"])

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        output_file = os.path.join(dest_dir, 'index.html')

        open(output_file, 'w').write(o.encode("utf-8"))

    shutil.copy(os.path.join(output_dir, content_list[-1]["name"], "index.html"), output_dir)

def main():

    content_list = get_content_list()

    template_loader = FileSystemLoader(template_dir)
    env = Environment(autoescape=False, loader=template_loader)

    gen_html_pages(content_list, env)

if __name__ == '__main__':
    main()

