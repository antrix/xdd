# OVERVIEW

This is a simple static site generator for http://devdriven.by/

The core of it is a `compile.py` script that takes json formatted files from the `content` directory and generates html files using Jinja `templates`.

A build script -- `make.sh` --  invokes the above and then merges the output of that with the contents of a `static` directory. The final output is contained in the `public` directory which should be suitable for serving by any web server capable of serving static files.

# LICENSE

All files in this repository are Copyright Deepak Sarda _except_ for the following files which are made available under the standard [MIT license][1].

* `make.sh`
* `compile.py`
* `static/js/xdd.js`

The intention is to encourage re-use and sharing of _code_ without facilitating whole-sale ripoffs of the website.

[1]: http://opensource.org/licenses/MIT
