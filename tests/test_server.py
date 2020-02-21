
import sh


def test_run_server_func():
    from asd.server import run_server
    def print_message(message):
        print(message)
    run_server(host='127.0.01', port=8000, publish=print_message)

def test_run_server_cmd():
    cmd = """python -m asd.server run-server -h '127.0.0.1' -p 8000 'rabbitmq://127.0.0.1:5672/'"""
    sh.bash(cmd)
