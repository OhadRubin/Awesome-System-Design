import pytest
import sh

@pytest.fixture
def packet():
    import asd.asd_pb2
    reader = asd.reader.Reader("asd/sample.mind.gz")

    el = next(iter(reader))
    user = asd.asd_pb2.User(user_id=reader.user_id,
                            username=reader.username,
                            birthday=reader.birthday,
                            gender=reader.gender)
    packet = asd.asd_pb2.Packet(snapshot=el, user=user).SerializeToString()
    return packet


def test_run_parser_import_pose(packet):
    from asd.parsers import run_parser

    run_parser('pose', packet)


def test_run_parser_import_feelings(packet):
    from asd.parsers import run_parser

    run_parser('feelings', packet)


def test_run_parser_import_color_image(packet):
    from asd.parsers import run_parser

    run_parser('color_image', packet)


def test_run_parser_import_depth_image(packet):
    from asd.parsers import run_parser

    run_parser('depth_image', packet)

def test_run_raw_data():
    cmd = """python -m asd.parsers parse 'pose' 'snapshot.raw' > 'pose.result'"""
    sh.bash(cmd)
    # assert False


def test_run_parser_cli():
    cmd = """python -m asd.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:5672/'"""
    sh.bash(cmd)
    # assert False 


