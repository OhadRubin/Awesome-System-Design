from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful import fields, marshal_with, reqparse, Resource
from asd.utils import asd_pb2
from flask_restful import reqparse
import click
from asd import parsers
from asd.utils import mq
from asd.utils.logger import Log



log = Log()

@click.group()
# @click.version_option(asd.version)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    log.quiet = quiet
    log.traceback = traceback


def run_server(host, port, publish):
    app = Flask(__name__)
    api = Api(app)

    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=int)
    parser.add_argument('username')
    parser.add_argument('birthday')
    parser.add_argument('gender')

    class Config(Resource):

        def get(self):
            args = parser.parse_args()
            return {"data": args, "parsers": parsers.snapshot_fields}

        def post(self):
                
            packet = asd_pb2.Packet.FromString(request.data)
            publish(packet.SerializeToString())
            #TODO: what goes here?
            return {"form": "hi"}

    api.add_resource(Config, '/config')
    app.run(host=host, port=port)

import time

# print("Printed immediately.")


@main.command('run-server')
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default="8000")
@click.argument('url', default="127.0.0.1")
# @click.argument('url', default="rabbitmq://127.0.0.1:5672")
def run_server_cli(host, port, url):
    while(True):
        try:
            channel, _ = mq.connect2exchange(addr=url)
            def publish2exchange(packet):
                channel.basic_publish(exchange='packet', routing_key='', body=packet)

            run_server(host, port, publish2exchange)
        except:
            continue






if __name__ == '__main__':
    main(prog_name='asd')