from pytest_httpserver import HTTPServer


def test_client():
    from asd.client import upload_sample
    with HTTPServer(host='127.0.0.1', port=8000) as httpserver:
        httpserver.expect_request("/config").respond_with_json({"parsers": ["pose"]})
        upload_sample(host='127.0.0.1', port=8000, path='scaffolding_files/tiny.mind.gz')



# def test_client_upload_sample_cli():
#     # cmd = """python -m asd.client upload-sample -h 127.0.0.1 --port 8000 asd/sample.mind.gz"""
#     cmd = """python -m asd.client upload-sample -h 127.0.0.1 --port 8000 asd/tiny.mind.gz"""
#
#     sh.bash(cmd)
    # assert False

