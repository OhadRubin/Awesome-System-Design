from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful import fields, marshal_with, reqparse, Resource
import click


@click.group()
# @click.version_option(asd.version)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    pass
    # log.quiet = quiet
    # log.traceback = traceback


def run_server(host, port):
    app = Flask(__name__)
    api = Api(app)

    class GetUsers(Resource):

        def get(self):
            return {'res': 'inside GetUsers'}

    api.add_resource(GetUsers, '/users')

    class GetUserDetails(Resource):
        def get(self, user_id):
            return {'res': f'inside GetUserDetails, for {user_id}'}

    api.add_resource(GetUserDetails, '/users/<user_id>')

    class GetUserSnapshotList(Resource):
        def get(self, user_id):
            return {'res': f'inside GetUserSnapshotList, for {user_id}'}

    api.add_resource(GetUserSnapshotList, '/users/<user_id>/snapshots')

    class GetUserSnapshot(Resource):
        def get(self, user_id, snapshot_id):
            return {'res': f'inside GetUserSnapshot, for {user_id}, from snapshot {snapshot_id}'}

    api.add_resource(GetUserSnapshot, '/users/<user_id>/snapshots/<snapshot_id>')

    class GetParserResult(Resource):
        def get(self, user_id, snapshot_id, result_name):
            res = f"""inside GetParserResult, for {user_id}, from snapshot {snapshot_id}, asked {result_name}"""
            return {'res': res, 'data': "TODO: data_url"}

    api.add_resource(GetParserResult, '/users/<user_id>/snapshots/<snapshot_id>/<result_name>')

    app.run(host=host, port=port)


@main.command('run-server')
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default="5000")
# @click.argument('url', default="127.0.0.1")
def run_server_cli(host, port):
    run_server(host, port)

if __name__ == '__main__':
    main(prog_name='asd')