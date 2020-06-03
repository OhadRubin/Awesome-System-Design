from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import click
import sh
from sqlalchemy.schema import CreateTable
from asd.utils.logger import Log
log = Log()

# MAPPING = {}
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    birthday = Column(String)
    gender = Column(String)


class Snapshot(Base):
    __tablename__ = 'snapshot'
    element_id = Column(Integer, primary_key=True)
    snapshot_id = Column(String)
    timestamp = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    user = relationship("User")
    parser_name = Column(String)
    parser_id = Column(Integer)



class Pose(Base):
    __tablename__ = 'pose'
    snapshot_id = Column(String, ForeignKey('snapshot.snapshot_id'), primary_key=True)
    snapshot = relationship("Snapshot")

    t_x = Column(Float)
    t_y = Column(Float)
    t_z = Column(Float)
    r_x = Column(Float)
    r_y = Column(Float)
    r_z = Column(Float)
    r_w = Column(Float)
# MAPPING[Pose.__tablename__] = Pose 


class DepthImage(Base):
    __tablename__ = 'depth_image'
    snapshot_id = Column(String, ForeignKey('snapshot.snapshot_id'), primary_key=True)
    snapshot = relationship("Snapshot")

    path = Column(String)
    width = Column(Integer)
    height = Column(Integer)
# MAPPING[DepthImage.__tablename__] = DepthImage 

class ColorImage(Base):
    __tablename__ = 'color_image'
    snapshot_id = Column(String, ForeignKey('snapshot.snapshot_id'), primary_key=True)
    snapshot = relationship("Snapshot")
    path = Column(String)
    width = Column(Integer)
    height = Column(Integer)
# MAPPING[DepthImage.__tablename__] = DepthImage 

class Feelings(Base):
    __tablename__ = 'feelings'
    snapshot_id = Column(String, ForeignKey('snapshot.snapshot_id'), primary_key=True)
    snapshot = relationship("Snapshot")

    hunger = Column(Float)
    thirst = Column(Float)
    exhaustion = Column(Float)
    happiness = Column(Float)
# MAPPING[Feelings.__tablename__] = Feelings 

MAPPING = {'pose': Pose, "depth_image": DepthImage,
                "color_image": ColorImage, "feelings": Feelings}

@click.group()
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    log.quiet = quiet
    log.traceback = traceback

def create_db(address):
    engine = create_engine(address)
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)

@main.command('create-db')
@click.option('-a', '--address', default="sqlite:///./data/asd.sqlite")
def create_db_cli(address):
    create_db(address)

@main.command('delete-db')
def delete_db():
    sh.rm("-rf",'data')
    sh.mkdir("data")

@main.command('reset-db')
@click.option('-a', '--address', default="sqlite:///./data/asd.sqlite")
def reset_db(address):
    sh.rm('./data/asd.sqlite')
    create_db(address)

if __name__ == '__main__':
    main(prog_name='asd')
