from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful import fields, marshal_with, reqparse, Resource
from . import asd_pb2
from flask_restful import reqparse
import click
from . import parsers
from . import mq


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
    pass
    # log.quiet = quiet
    # log.traceback = traceback


@main.command('run-server')
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default="8000")
@click.argument('url', default="rabbitmq://127.0.0.1:5672")
def run_server(host, port, url):
    channel, _ = mq.connect2exchange()

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

            channel.basic_publish(exchange='packet', routing_key='', body=packet.SerializeToString())
            return {"form": "hi"}

    api.add_resource(Config, '/config')
    app.run(host=host, port=port, debug=True)


if __name__ == '__main__':
    main(prog_name='asd')