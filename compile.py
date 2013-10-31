#!/usr/bin/env python

import iso8601
import json
import os
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

template_loader = FileSystemLoader(template_dir)
env = Environment(autoescape=False, loader=template_loader)
template = env.get_template("index.jnj")

content_files = ((f, os.path.join(os.getcwd(), content_dir, f)) for f in os.listdir(content_dir) if f.endswith(content_ext))

context_list = []

for f, fpath in content_files:
    #print "Now file:", f
    fname, ext = os.path.splitext(f)

    context = json.loads(open(fpath).read())

    context["date"] = iso8601.parse_date(context["date"])
    context["name"] = fname
    context["slug"] = "/%s/" % (fname,)

    context_list.append(context)

context_list.sort(key=lambda c: c["date"])

for idx, context in enumerate(context_list):
    context["prev_slug"] = context_list[idx - 1]["slug"] if idx > 0 else None
    context["next_slug"] = context_list[idx + 1]["slug"] if idx < len(context_list) - 1 else None


for context in context_list:
    #print "Now name:", context["name"], context["date"]

    o = template.render(context)

    dest_dir = os.path.join(os.getcwd(), output_dir, context["name"])

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    open(os.path.join(dest_dir, 'index.html'), 'w').write(o.encode("utf-8"))

