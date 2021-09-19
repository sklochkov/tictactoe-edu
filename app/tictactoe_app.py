#!/usr/bin/env python3
import flask
from uuid import uuid4 as uuid
import re
from random import choice
from flask import json
from werkzeug.wrappers import response
from game import Game

SANITIZE_NICKNAME_RE = re.compile(r"[^A-Za-z0-9\-_=+\.]")

DEFAULT_ADJ = ["Cool", "Funny", "Little", "Cute"]
DEFAULT_NAME = ["Cat", "Dog", "Hamster", "Parrot"]


def sanitize_nickname(username):
    res = SANITIZE_NICKNAME_RE.sub('', username)
    if not res:
        return choice(DEFAULT_ADJ) + choice(DEFAULT_NAME)
    return res


def gen_game_code():
    name = ''
    for i in range(4):
        name += chr(65 + choice(range(26)))
    return name


def gen_game(user_id, username):
    game_code = gen_game_code()
    while game_code in app.games:
        game_code = gen_game_code()
    app.games[game_code] = Game(user_id, username)
    return game_code


class TictactoeApp(flask.Flask):
    def __init__(self, *args, **kwargs):
        super(TictactoeApp, self).__init__(*args, **kwargs)
        self.games = {}


app = TictactoeApp(__name__)


@app.route('/api/ping')
def ping():
    return 'pong'


@app.route('/api/signup', methods=['POST'])
def signUp():
    username = sanitize_nickname(flask.request.form.get('username', '')[:100])
    user_type = flask.request.form.get('user_type')
    game_code = flask.request.form.get('game_code')
    res = flask.make_response('', 302)
    if flask.request.cookies.get('ID'):
        user_id = flask.request.cookies.get('ID')
    else:
        user_id = str(uuid())
        res.set_cookie(b'ID', bytes(user_id, 'utf-8'))
    if username != flask.request.cookies.get('username'):
        res.set_cookie(b'username', bytes(username, 'utf-8'))
    if user_type == "first" and not game_code:
        game_code = gen_game(user_id, username)
    elif user_type == "first" and game_code:
        res.headers['Location'] = (flask.request.environ['REQUEST_SCHEME']
                                   + '://'
                                   + flask.request.environ['HTTP_HOST']
                                   + '/ERROR')
        return res
    else:
        if game_code in app.games:
            if (app.games[game_code].check_player(user_id) == 0 and
                    not app.games[game_code].second_player):
                app.games[game_code].set_second_player(user_id, username)
            else:
                res.headers['Location'] = (
                    flask.request.environ['REQUEST_SCHEME']
                    + '://'
                    + flask.request.environ['HTTP_HOST']
                    + '/OCCUPIED')
                return res
        else:
            res.headers['Location'] = (flask.request.environ['REQUEST_SCHEME']
                                       + '://'
                                       + flask.request.environ['HTTP_HOST']
                                       + '/NO_GAME')
            return res
    res.headers['Location'] = (flask.request.environ['REQUEST_SCHEME']
                               + '://'
                               + flask.request.environ['HTTP_HOST']
                               + f'/{game_code}')
    return res


@app.route('/api/<game_code>/data', methods=['GET', 'POST'])
def data(game_code):
    user_id = flask.request.cookies.get('ID')
    player = app.games[game_code].check_player(user_id)
    if flask.request.method == 'GET':
        res = {}
        if player != 0:
            if player == 1:
                opponent_username = app.games[game_code].second_player['username']
            else:
                opponent_username = app.games[game_code].first_player['username']
            res = ({'game_board': app.games[game_code].board,
                    'game_state': app.games[game_code].game_over(),
                    'current_player': app.games[game_code].current_player(),
                    'opponent_username': opponent_username})
            return json.dumps(res)
        else:
            res = flask.make_response('', 302)
            res.headers['Location'] = (
                    flask.request.environ['REQUEST_SCHEME']
                    + '://'
                    + flask.request.environ['HTTP_HOST']
                    + '/OCCUPIED')
            return res
    elif flask.request.method == 'POST':
        res = ""
        col = flask.request.form.get('pos_x')
        row = flask.request.form.get('pos_y')
        if col.isdigit() and row.isdigit() and len(row) == 1 and len(col) == 1:
            col = int(col)
            row = int(row)
        else:
            return "ERROR", 400
        if (player != 0 and
            app.games[game_code].current_player() == user_id and
            col >= 0 and col <= 2 and row >= 0 and row <= 2 and
            app.games[game_code].board[row * 3 + col] == 0):
            app.games[game_code].make_move(col, row, user_id)
            res = flask.make_response('', 200)
            return res
        else:
            return "ERROR", 400
