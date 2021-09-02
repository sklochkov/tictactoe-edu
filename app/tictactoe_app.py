#!/usr/bin/env python3
import flask

class TictactoeApp(flask.Flask):
    def __init__(self, *args, **kwargs):
        super(TictactoeApp, self).__init__(*args, **kwargs)

app = TictactoeApp(__name__)

@app.route('/api/ping')
def ping():
    return "pong"

