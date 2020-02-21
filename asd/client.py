import requests
from .reader import Reader
from . import asd_pb2
import click
import sh
import os

class Log:
    def __init__(self):
        self.quiet = False
        self.traceback = False

    def __call__(self, message):
        if self.quiet:
            return
        if self.traceback and sys.exc_info():  # there's an active exception
            message += os.linesep + traceback.format_exc().strip()
        click.echo(message)


log = Log()


@click.group()
# @click.version_option(asd.version)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    log.quiet = quiet
    log.traceback = traceback

@main.command('upload-sample')
@click.option('-h', '--host', default='http://127.0.0.1')
@click.option('-p', '--port', default=8000)
@click.argument('path')
def upload_sample(host, port, path):
    addr = f"{host}:{port}"
    reader = Reader(path)
    user_fields = {"user_id": reader.user_id, "username": reader.username,
                   "birthday": reader.birthday, "gender": reader.gender}

    user = asd_pb2.User(**user_fields)

    for i, snapshot in enumerate(reader):
        resp_result = requests.get(f'{addr}/config', data=user_fields).json()
        available_parsers = resp_result['parsers']
        snapshot_fields = {"color_image": snapshot.color_image,
                           "pose": snapshot.pose,
                           "depth_image": snapshot.depth_image,
                           "feelings": snapshot.feelings}

        snapshot = asd_pb2.Snapshot(**{parser_name: snapshot_fields[parser_name]
                                       for parser_name in available_parsers})
        packet = asd_pb2.Packet(snapshot=snapshot, user=user).SerializeToString()
        resp = requests.post(f'{addr}/config', data=packet,
                             headers={'Content-Type': 'application/protobuf',
                                      'Content-Length': str(len(packet))})
        print(resp)
        #TODO: fail gracefuly
        # break

if __name__ == '__main__':
    main(prog_name='asd')
