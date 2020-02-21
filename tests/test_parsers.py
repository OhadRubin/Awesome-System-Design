import pytest
import sh


def test_run_parser_import():
    # assert False
    from asd.parsers import run_parser
    data = None
    result = run_parser('pose', data)
    # assert result


def test_run_raw_data():
    cmd = """python -m asd.parsers parse 'pose' 'snapshot.raw' > 'pose.result'"""
    sh.bash(cmd)
    # assert False


def test_run_parser_cli():
    cmd = """python -m asd.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:5672/'"""
    sh.bash(cmd)
    # assert False 


