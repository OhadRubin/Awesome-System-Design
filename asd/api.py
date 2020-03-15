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
from asd.db import User, Base, Snapshot, ColorImage, DepthImage, Pose, Feelings, create_db, MAPPING
from sqlalchemy import text
from asd import mq
import json
from datetime import datetime
import base64

@click.group()
# @click.version_option(asd.version)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    pass
    # log.quiet = quiet
    # log.traceback = traceback

def dictify(x):
    return {col.name: x.__dict__[col.name] for col in x.__table__.columns}

def run_server(host, port, database_url):
    engine = create_engine(database_url)
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    app = Flask(__name__)
    api = Api(app)

    class GetUsers(Resource):
        def get(self):
            users = session.query(User).all()
            return {'res': [dictify(user) for user in users]}

    api.add_resource(GetUsers, '/users')

    class GetUserDetails(Resource):
        def get(self, user_id):
            user = session.query(User).filter(User.user_id == int(user_id)).first()
            return {'res':  dictify(user)}

    api.add_resource(GetUserDetails, '/users/<user_id>')

    class GetUserSnapshotList(Resource):

        def get(self, user_id):
            snapshots = session.query(Snapshot).filter(Snapshot.user_id == int(user_id)).group_by(Snapshot.snapshot_id).all()
            return {'res': [dict(snapshot_id=snapshot.snapshot_id, timestamp=snapshot.timestamp) for snapshot in snapshots]}

    api.add_resource(GetUserSnapshotList, '/users/<user_id>/snapshots')

    class GetUserSnapshot(Resource):
        def get(self, user_id, snapshot_id):
            snapshots = session.query(Snapshot).filter(Snapshot.user_id == int(user_id))\
                                               .filter(Snapshot.snapshot_id == snapshot_id).all()
            if snapshots:
                res = dict(snapshot_id=snapshots[0].snapshot_id, timestamp=snapshots[0].timestamp, parsers=[])
                for parser in snapshots:
                    res['parsers'].append(parser.parser_name)
                return {'res': res}
            else:
                return {}

    api.add_resource(GetUserSnapshot, '/users/<user_id>/snapshots/<snapshot_id>')

    class GetParserResult(Resource):
        def get(self, user_id, snapshot_id, result_name):
            parser_result = session.query(MAPPING[result_name]).\
                filter(MAPPING[result_name].snapshot_id == snapshot_id).first()
            return {'res': dictify(parser_result)}

    api.add_resource(GetParserResult, '/users/<user_id>/snapshots/<snapshot_id>/<result_name>')

    class GetParserResultData(Resource):
        def get(self, user_id, snapshot_id, result_name):
            parser_result = session.query(MAPPING[result_name]).\
                filter(MAPPING[result_name].snapshot_id == snapshot_id).first()
            if "path" in parser_result.__dict__:
                with open(parser_result.path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                return {'res': encoded_string.decode('utf-8')}
            else:
                return {"res":''}

    api.add_resource(GetParserResultData, '/users/<user_id>/snapshots/<snapshot_id>/<result_name>/data')

    app.run(host=host, port=port)

@main.command('run-server')
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default="5000")
@click.option('-d', '--database', default="sqlite:///./data/asd.sqlite")
def run_server_cli(host, port, database):
    print("api ready")
    run_server(host, port, database_url=database)

if __name__ == '__main__':
    main(prog_name='asd')