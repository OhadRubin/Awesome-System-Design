# from . import asd_pb2
import click

from asd.parsers import run_parser, parse
import os
from asd.utils import mq



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
def parse_cli(parser_name, path):
    print(parse(parser_name, path))

import time
@main.command('run-parser')
@click.argument('parser_name')
@click.argument('url')
def run_parser_mq(parser_name, url):
    # time.sleep(10)
    print("hi")
    out_channel, _ = mq.connect2exchange(addr=url, exchange_name="worker")
    in_channel, queue_name = mq.connect2exchange(addr=url, exchange_name='packet')

    def parse_f(channel, method, propreties, body):
        print("parser_name")
        res = run_parser(parser_name, packet=body)
        out_channel.basic_publish(exchange="worker", routing_key='', body=res)
        # print(res)
        #TODO add log with: print(res)
        return res

    in_channel.basic_consume(
        queue=queue_name, on_message_callback=parse_f, auto_ack=True)
    in_channel.start_consuming()

if __name__ == '__main__':
    main(prog_name='asd')
