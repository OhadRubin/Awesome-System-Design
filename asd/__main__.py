import os
import sys
import traceback
import datetime as dt
import click
from asd.utils import Connection, Listener
import asd

from pathlib import Path

def write_thought(dir,thought):
    prev_thoughts=''
    time_stamp = str(thought.timestamp).replace(" ","_").replace(":","-")
    if Path(f'{dir}/{thought.user_id}/{time_stamp}.txt').exists():
        with open(f'{thought.dir}/{thought.user_id}/{time_stamp}.txt','r') as f:  
            prev_thoughts = f.readlines()
    with open(f'{dir}/{thought.user_id}/{time_stamp}.txt','w+') as f:  
        if not prev_thoughts:
            f.write(thought.thought)
        else:
            for t in prev_thoughts:
                f.write(t+"\n")
            f.write(thought.thought+"\n")

class Log:
    def __init__(self):
        self.quiet = False
        self.traceback = False
    def __call__(self, message):
        if self.quiet:
            return
        if self.traceback and sys.exc_info(): # there's an active exception
            message += os.linesep + traceback.format_exc().strip()
        click.echo(message)
log = Log()

@click.group()
@click.version_option(asd.version)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    log.quiet = quiet
    log.traceback = traceback
    

@main.command('upload_thought')
@click.option('-a', '--host', default = '127.0.0.1')
@click.option('-p', '--port', default = 8000)
@click.option('-u', '--user_id',required=True)
@click.option('-t', '--thought',required=True)
def upload_thought(host, port, user_id, thought):
    thought = asd.Thought(user_id, dt.datetime.now(), thought)
    with Connection.connect(host, port) as connection:
        connection.send(thought.serialize())


@main.command('run_server')
@click.option('-a', '--host', default = '127.0.0.1')
@click.option('-p', '--port', default = 8000)
@click.option('-d', '--dir',required=True)
def run_server(host, port, dir):
    try:
        while True:
            with Listener(port,host) as conn:
                data = conn.receive_all()
                thought = asd.Thought.deserialize(data)
                write_thought(dir,thought)

    except KeyboardInterrupt:
        return 0
    

@main.command('run_webserver')
@click.option('-a', '--host', default = '127.0.0.1')
@click.option('-p', '--port', default = 8001)
@click.option('-d', '--dir',required=True)
def _run_webserver(host, port, dir):
    from asd import web 
    web.run_webserver((host, port),dir)


if __name__ == '__main__':
    main(prog_name='asd')
    # try:
    # except Exception as error:
    #     log(f'ERROR: {error}')
    #     sys.exit(1)
