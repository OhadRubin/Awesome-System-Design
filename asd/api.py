from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful import fields, marshal_with, reqparse, Resource
import click
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import click
from asd.db import *
from asd.db import User, Base, Snapshot, ColorImage, DepthImage, Pose, Feelings, create_db
from asd import mq
import json
from datetime import datetime

@click.group()
# @click.version_option(asd.version)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    pass
    # log.quiet = quiet
    # log.traceback = traceback


def run_server(host, port, database_url):
    engine = create_engine(database_url)
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    app = Flask(__name__)
    api = Api(app)

    class GetUsers(Resource):

        def get(self):
            return {'res': session.query(User).all()}

    api.add_resource(GetUsers, '/users')

    class GetUserDetails(Resource):
        def get(self, user_id):
            return {'res': session.query(User).filter(User.user_id == int(user_id)).all()}

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
import time

@main.command('run-server')
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default="5000")
@click.option('-d', '--database', default='sqlite:///asd_db.sqlite')
def run_server_cli(host, port, database):
    # time.sleep(30)
    # create_db(database)
    print("api ready")
    run_server(host, port, database_url=database)

if __name__ == '__main__':
    main(prog_name='asd')