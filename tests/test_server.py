import multiprocessing
import time


def test_server():
    from asd.client import upload_sample
    from asd.server import run_server

    def print_message(message):
        print(message)

    server = multiprocessing.Process(target=run_server, kwargs=dict(host='127.0.01', port=8000, publish=print_message))
    server.start()
    upload_sample(host='127.0.0.1', port=8000, path='asd/tiny.mind.gz')
    time.sleep(0.03)
    server.terminate()

# def test_run_server_cmd():
#     """docker run -d -p 5672:5672 rabbitmq"""
#     cmd = """python -m asd.server run-server -h '127.0.0.1' -p 8000 'rabbitmq://127.0.0.1:5672/'"""
#     cmd = """python -m asd.server run-server -h '127.0.0.1' -p 8000 127.0.0.1"""

#     sh.bash(cmd)

