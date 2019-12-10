import os
import sys
import traceback
import datetime as dt
import click
from asd.utils import Connection, Listener
import .web 


@foo.command('upload_thought')
@click.option('-a', '--host', default = '127.0.0.1')
@click.option('-p', '--port', default = 8000)
@click.option('-u', '--user_id')
@click.option('-t', '--thought')
def upload_thought(host, port, user_id, thought):
    thought = Thought(user_id, dt.datetime.now(), thought)
    with Connection.connect(host, port) as connection:
        connection.send(thought.serialize())


@foo.command('run_server')
@click.option('-a', '--host', default = '127.0.0.1')
@click.option('-p', '--port', default = 8000)
def run_server(host, port):
    try:
        with Listener.connect(host, port) as listener:
            while True:
                listener.accept()
    except KeyboardInterrupt:
        return 0

@foo.command('run_webserver')
@click.option('-a', '--host', default = '127.0.0.1')
@click.option('-p', '--port', default = 8001)
@click.option('-d', '--dir')
def _run_webserver(host, port, dir):
    web.run_webserver((host, port),dir)
