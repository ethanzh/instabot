from flask import Flask, render_template, url_for, jsonify
import sqlite3
import json

app = Flask(__name__, static_url_path='')


@app.route('/')
def hello_world():
    username = get_new_username()
    if username is not None:
        return render_template("index.html", initial=username)
    else:
        return render_template("index.html")


@app.route('/rate/<string:username>/<int:rating>/')
def set_value(username, rating):
    with sqlite3.connect('accounts.db') as conn:
        c = conn.cursor()
        c.execute('UPDATE accounts SET fake = %d WHERE username = \'%s\'' % (rating, username))
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/new/')
def get_new():
    username = get_new_username()
    if username is not None:
        return json.dumps({'url': str(url_for('static', filename='screenshots/%s.jpeg' % username))}), \
                        200, {'ContentType': 'text/plain'}
    else:
        return json.dumps({'url': "empty"}), 200, {'ContentType': 'text/plain'}


def get_new_username():
    with sqlite3.connect('accounts.db') as conn:
        c = conn.cursor()
        username = c.execute('SELECT username FROM accounts WHERE fake = -1 LIMIT 1')
        try:
            username = username.fetchall()[0][0]
            return username
        except IndexError:
            return None
