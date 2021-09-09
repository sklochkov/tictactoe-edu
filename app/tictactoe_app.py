#!/usr/bin/env python3
import flask
from uuid import uuid4 as uuid
import re
from random import choice

SANITIZE_NICKNAME_RE = re.compile(r"[^A-Za-z0-9\-_=+\.]")

DEFAULT_ADJ = ["Cool", "Funny", "Little", "Cute"]
DEFAULT_NAME = ["Cat", "Dog", "Hamster", "Parrot"]


def sanitize_nickname(username):
    res = SANITIZE_NICKNAME_RE.sub('', username)
    if not res:
        return choice(DEFAULT_ADJ) + choice(DEFAULT_NAME)
    return res

class TictactoeApp(flask.Flask):
    def __init__(self, *args, **kwargs):
        super(TictactoeApp, self).__init__(*args, **kwargs)

app = TictactoeApp(__name__)

@app.route('/api/ping')
def ping():
    return 'pong'

@app.route('/api/signup', methods=['POST'])
def signUp():
    username = sanitize_nickname(flask.request.form.get('username'))
    
    res = flask.make_response('', 302)
    res.headers['Location'] = flask.request.environ['REQUEST_SCHEME'] + '://' + flask.request.environ['HTTP_HOST'] + '/GAME_CODE'
    res.set_cookie(b'ID', bytes(str(uuid()), 'utf-8'))
    res.set_cookie(b'username', bytes(username, 'utf-8'))
    return res


