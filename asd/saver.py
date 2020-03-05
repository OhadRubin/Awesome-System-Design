from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import click
from asd.db import *
from asd.db import User, Base, Snapshot
from asd import mq


class Saver:
    def __init__(self, database_url):
        engine = create_engine(database_url)
        Base.metadata.bind = engine

        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def save(self, parser_name, data):
        user = User(id=1, username="hi")
        snapshot = Snapshot(id=1, username="hi")
        self.session.add(user)
        self.session.add(snapshot)
        self.session.commit()


@click.group()
# @click.version_option(asd.version)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    pass


@main.command('save')
@click.argument('pika_url')
@click.argument('database_url', default='sqlite:///asd_db.sqlite')
def save_cli(pika_url, database_url):
    channel, queue_name = mq.connect2exchange(addr=pika_url, exchange_name='worker')

    saver = Saver(database_url=database_url)
    def handle_msg(channel, method, propreties, body):
        saver.save(parser_name=body['parser_name'], data=body['data'])

    channel.basic_consume(
        queue=queue_name, on_message_callback=handle_msg, auto_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    main(prog_name='asd')