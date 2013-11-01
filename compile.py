#!/usr/bin/env python

import iso8601
import json
import os
import shutil

from jinja2 import Environment, FileSystemLoader

## Start configuration options ##
site_url = "http://devdriven.by"
# directory where to start looking for templates
content_dir = os.path.join(os.getcwd(), 'content')
# directory where to save generated files
output_dir = os.path.join(os.getcwd(), 'public')
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

    # oldest first
    content_list.sort(key=lambda c: c["date"])

    for idx, context in enumerate(content_list):
        context["prev_slug"] = content_list[idx - 1]["slug"] if idx > 0 else None
        context["next_slug"] = content_list[idx + 1]["slug"] if idx < len(content_list) - 1 else None

    return content_list


def gen_html_pages(content_list, jinja_env):

    template = jinja_env.get_template("index.jnj")

    for content in content_list:
        #print "Now name:", context["name"], context["date"]

        o = template.render(content)

        dest_dir = os.path.join(output_dir, content["name"])

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        output_file = os.path.join(dest_dir, 'index.html')
        open(output_file, 'w').write(o.encode("utf-8"))

        json_todump = dict(content)
        json_todump["date"] = json_todump["date"].isoformat('T') 

        json_file = open(os.path.join(dest_dir, 'index.json'), 'w')
        json.dump(json_todump, json_file, separators=(',',':'))
        json_file.close()

    shutil.copy(os.path.join(output_dir, content_list[-1]["name"], "index.html"), output_dir)
    shutil.copy(os.path.join(output_dir, content_list[-1]["name"], "index.json"), output_dir)

def gen_atom_feed(content_list, jinja_env):

    # latest first
    aphorisms = sorted(content_list, key=lambda c: c["date"], reverse=True)

    template = jinja_env.get_template("feed.jnj")

    o = template.render(aphorisms=aphorisms, site_url=site_url)

    dest_dir = os.path.join(output_dir, "feed")
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    output_file = os.path.join(dest_dir, 'index.atom')

    open(output_file, 'w').write(o.encode("utf-8"))

def main():

    content_list = get_content_list()

    template_loader = FileSystemLoader(template_dir)
    env = Environment(autoescape=False, loader=template_loader)

    gen_html_pages(content_list, env)

    gen_atom_feed(content_list, env)

if __name__ == '__main__':
    main()

