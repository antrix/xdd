import os

from flask import Flask, render_template, g, abort, json, jsonify, url_for

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
@app.route('/<slug>')
def index(slug=None):

    if slug:
        aphorism = r.table('aphorisms').get(slug).run(g.rdb_conn)
        if not aphorism:
            abort(404)

    random_aphorisms = get_random_aphorisms(g.rdb_conn)

    if not slug:
        aphorism = random_aphorisms.pop()

    return render_template('index.html', aphorism=aphorism, preloaded_aphorisms=json.dumps(random_aphorisms))

@app.route('/a/get_random')
def api_get_random():
    random_aphorisms = get_random_aphorisms(g.rdb_conn)
    return jsonify({'Aphorisms': random_aphorisms})


def get_random_aphorisms(rdb_conn):
    random_aphorisms = list(r.table('aphorisms').sample(10).run(rdb_conn))

    for ap in random_aphorisms:
        ap['permalink'] = url_for('index', slug=ap['slug'])

    return random_aphorisms

if __name__ == '__main__':
    app.run(debug=True)
