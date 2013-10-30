#!/usr/bin/env python

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

for f, fpath in content_files:
    print "Now file:", f
    fname, ext = os.path.splitext(f)

    context = json.loads(open(fpath).read())
    context["slug"] = "/%s/" % (fname,)

    o = template.render(context)

    dest_dir = os.path.join(os.getcwd(), output_dir, fname)

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    open(os.path.join(dest_dir, 'index.html'), 'w').write(o.encode("utf-8"))

