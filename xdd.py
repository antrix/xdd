import os

from flask import Flask, render_template, g, abort, json, jsonify, url_for

import thedb

app = Flask(__name__)

@app.route('/')
@app.route('/<slug>')
def index(slug=None):

    if slug:
        aphorism = thedb.get(slug)
        if not aphorism:
            abort(404)

    random_aphorisms = get_random_aphorisms()

    if not slug:
        aphorism = random_aphorisms.pop()

    return render_template('index.html', aphorism=aphorism, preloaded_aphorisms=json.dumps(random_aphorisms))

@app.route('/a/get_random')
def api_get_random():
    random_aphorisms = get_random_aphorisms()
    return jsonify({'Aphorisms': random_aphorisms})


def get_random_aphorisms():
    random_aphorisms = thedb.get_random(10)

    for ap in random_aphorisms:
        ap['permalink'] = url_for('index', slug=ap['slug'])

    return random_aphorisms

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
