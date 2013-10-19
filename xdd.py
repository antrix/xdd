import os

from flask import Flask, render_template, g, abort

import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

RDB_HOST =  os.environ.get('RDB_HOST') or 'localhost'
RDB_PORT = os.environ.get('RDB_PORT') or 28015
RDB_DB = 'xdd'

app = Flask(__name__)

@app.before_request
def before_request():
    try:
        g.rdb_conn = r.connect(host=RDB_HOST, port=RDB_PORT, db=RDB_DB)
    except RqlDriverError:
        abort(503, "No database connection could be established.")

@app.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.close()
    except AttributeError:
        pass

@app.route('/')
@app.route('/<aphorism>')
def index(aphorism=None):
    if aphorism:
        aphorism = r.table('aphorisms').get(aphorism).run(g.rdb_conn)
        if not aphorism:
            abort(404)
    else:
        aphorism = list(r.table('aphorisms').sample(1).run(g.rdb_conn))[0]

    return render_template('index.html', aphorism=aphorism)

if __name__ == '__main__':
    app.run(debug=True)
