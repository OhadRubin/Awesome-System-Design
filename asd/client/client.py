import requests
from asd.utils.reader import Reader
from asd.utils import asd_pb2
import click
import sh
import os
import time

from asd.utils.logger import Log


log = Log()


@click.group()
# @click.version_option(asd.version)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    log.quiet = quiet
    log.traceback = traceback
    log.setName("client")

def upload_sample(path, host, port,max_samples=-1,timeout=0):
    addr = f"http://{host}:{port}"
    reader = Reader(path)
    user_fields = {"user_id": reader.user_id, "username": reader.username,
                   "birthday": reader.birthday, "gender": reader.gender}

    user = asd_pb2.User(**user_fields)

    for i, snapshot in enumerate(reader):
        resp_result = requests.get(f'{addr}/config', data=user_fields).json()
        # TODO: check which parsers are online in server
        available_parsers = resp_result['parsers'] + ["datetime"]
        snapshot_fields = {"color_image": snapshot.color_image,
                           "pose": snapshot.pose,
                           "depth_image": snapshot.depth_image,
                           "feelings": snapshot.feelings,
                           "datetime": snapshot.datetime}

        snapshot = asd_pb2.Snapshot(**{parser_name: snapshot_fields[parser_name]
                                       for parser_name in available_parsers})
        packet = asd_pb2.Packet(snapshot=snapshot, user=user).SerializeToString()
        resp = requests.post(f'{addr}/config', data=packet,
                             headers={'Content-Type': 'application/protobuf',
                                      'Content-Length': str(len(packet))})
        # if timeout>0:
        time.sleep(0.05)
        if i==max_samples:
            break

@main.command('upload-sample')
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default=8000)
@click.option('-m', '--max_samples', default=-1)
@click.option('-t', '--timeout', default=0)
@click.argument('path')
def upload_sample_cli(path, host, port, max_samples,timeout):
    upload_sample(path, host, port, max_samples,timeout)

        #TODO: fail gracefuly
        # break

if __name__ == '__main__':
    main(prog_name='asd')
