import pytest
import sh


def test_client_upload_sample():
    from asd.client import upload_sample
    upload_sample(host='127.0.0.1', port=8000, path='asd/sample.mind.gz')

def test_client_upload_sample_cli():
    # cmd = """python -m asd.client upload-sample -h http://127.0.0.1 --port 8000 asd/sample.mind.gz"""
    cmd = """python -m asd.client upload-sample -h http://127.0.0.1 --port 8000 asd/tiny.mind.gz"""

    sh.bash(cmd)
    # assert False