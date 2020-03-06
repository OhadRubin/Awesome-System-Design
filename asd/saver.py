from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import click
from asd.db import *
from asd.db import User, Base, Snapshot, ColorImage, DepthImage, Pose, Feelings
from asd import mq
import json
from datetime import datetime

class Saver:
    def __init__(self, database_url):
        engine = create_engine(database_url)
        Base.metadata.bind = engine

        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
        self.mapping = {'pose': Pose, "depth_image": DepthImage,
                        "color_image": ColorImage, "feelings": Feelings}

    def save(self, parser_name, data):
        user = self.session.query(User).filter(User.user_id == data['user']['user_id']).first()
        if not user:
            user = User(**data['user'])

        snapshot = Snapshot(snapshot_id=f"{data['user']['user_id']}_{str(data['timestamp'])}",
                            timestamp=data['timestamp'],
                            parser_name=parser_name, user=user)
        row = self.mapping[parser_name](snapshot=snapshot, **data['result'])

        self.session.add(snapshot)
        self.session.add(row)
        self.session.commit()


@click.group()
# @click.version_option(asd.version)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    pass

@main.command('run-saver')
@click.argument('pika_url')
@click.argument('database_url', default='sqlite:///asd_db.sqlite')
def run_saver_cli(pika_url, database_url):
    channel, queue_name = mq.connect2exchange(addr=pika_url, exchange_name='worker')
    saver = Saver(database_url=database_url)

    def handle_msg(channel, method, propreties, body):
        body = json.loads(body)
        saver.save(parser_name=body['parser_name'], data=body['data'])

    channel.basic_consume(
        queue=queue_name, on_message_callback=handle_msg, auto_ack=True)
    channel.start_consuming()

@main.command('save')
@click.argument('database_url', default='sqlite:///asd_db.sqlite')
@click.argument('parser_name')
@click.argument('data_path')
def save_cli(database_url, parser_name, data_path):
    saver = Saver(database_url=database_url)
    with open(data_path) as f:
        body = json.load(f)
    saver.save(parser_name=body['parser_name'], data=body['data'])





if __name__ == '__main__':
    main(prog_name='asd')