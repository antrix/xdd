# OVERVIEW

This is a simple static site generator for <http://devdriven.by/>

The core of it is a `compile.py` script that takes json formatted files from the `content` directory and generates html files using Jinja `templates`.

A build script -- `make.sh` --  invokes the above and then merges the output of that with the contents of a `static` directory. The final output is contained in the `public` directory which should be suitable for serving by any web server capable of serving static files.

# LICENSE

All files in this repository are Copyright Deepak Sarda _except_ for the following files which are made available under the standard [MIT license][1].

* `make.sh`
* `compile.py`
* `static/js/xdd.js`

The intention is to encourage re-use and sharing of _code_ without facilitating wholesale ripoffs of the website.

[1]: http://opensource.org/licenses/MIT


# LOCAL DEVELOPMENT

Create a virtual environment:

    $ python3 -m venv venv 
    $ source venv/bin/activate
    $ pip install -r requirements.txt 

    $ ln -s public-dummy public # One time

Build and run local server:

    $ ./make.sh
    $ (cd public; python -m http.server)


# DEPLOY

On remote, create a new file `rebuild-site.sh` in the repo's git hooks directory:

    #!/bin/bash -e

    export HOME=/home/antrix
    TARGET_REPO=${HOME}/devdriven.by

    source ${HOME}/.bashrc
    source ${WORKON_HOME}/xdd/bin/activate

    echo "updating TARGET_REPO: ${TARGET_REPO}"

    cd ${TARGET_REPO} || exit 1

    env -i git pull
    ./make.sh

Invoke this `rebuild-site.sh` script during post receive by including the following line in the `post-receive` hook file:

    . /home/antrix/gitrepos/xdd.git/hooks/rebuild-site.sh

From local dev machine, push changes to remote:

    git push antrix@antrix.net:gitrepos/xdd.git

Thanks to the post receive hook, a website rebuild will be automatically triggered.
