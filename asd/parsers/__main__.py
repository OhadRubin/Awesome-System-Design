from . import asd_pb2
import click
from asd.parsers import parser_list
import os
from asd import mq

class Context:
    def __init__(self, user_id, timestamp):
        self.user_id = user_id
        self.timestamp = timestamp

    def path(self, filename):
        return f"data/{self.user_id}/{self.timestamp}/{filename}"

    def save(self, filename, data):
        filename = self.path(filename)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            f.write(data)


def run_parser(parser_name, packet):
    parse_method = parser_list[parser_name]
    packet = asd_pb2.Packet(packet)
    context = Context(user_id=packet.user.user_id, timestamp=packet.snapshot.datetime)
    res = parse_method(context=context, snapshot=packet.snapshot)
    return res


@click.group()
# @click.version_option(asd.version)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    pass


# TODO: add to documentation that we only accept .raw files,
#  otherwise we assume this is a byte array
@main.command('parse')
@click.argument('parser_name')
@click.argument('path')
def parse(parser_name, path):
    assert isinstance(path, str) and path.endswith(".raw")
    with open(path) as f:
        print(run_parser(parser_name, packet=f.read()))


@main.command('run-parser')
@click.argument('parser_name')
@click.argument('url')
def run_parser_mq(parser_name, url):
    def parse_f(s):
        return run_parser(parser_name, packet=s)
    channel, queue_name = mq.connect2exchange(addr=url)
    channel.basic_consume(
        queue=queue_name, on_message_callback=parse_f, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    main(prog_name='asd')
