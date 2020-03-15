import click
import requests

@click.group()
# @click.version_option(asd.version)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    pass
    # log.quiet = quiet
    # log.traceback = traceback

@main.command('get-users')
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default="5000")
def get_users(host, port):
    res = requests.get(f"http://{host}:{port}/users")
    print(res.json()['res'])


@main.command('get-user')
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default="5000")
@click.argument("user_id")
def get_user(host, port, user_id):
    res = requests.get(f"http://{host}:{port}/users/{user_id}")
    print(res.json()['res'])


@main.command('get-snapshots')
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default="5000")
@click.argument("user_id")
def get_snapshots(host, port, user_id):
    res = requests.get(f"http://{host}:{port}/users/{user_id}/snapshots")
    print(res.json()['res'])


@main.command('get-snapshot')
@click.option('-h', '--host', default='127.0.0.1')
@click.option('-p', '--port', default="5000")
@click.argument("user_id")
@click.argument("snapshot_id")
def get_snapshot(host, port, user_id, snapshot_id):
    res = requests.get(f"http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}")
    print(res.json()['res'])


@main.command('get-result')
@click.option('-h', '--host', default='0.0.0.0')
@click.option('-p', '--port', default="5000")
@click.option('-s',"--save", default='')
@click.argument("user_id")
@click.argument("snapshot_id")
@click.argument("result_name")
# @click.argument("path")
def get_result(host, port,save, user_id, snapshot_id, result_name):
    res = requests.get(f"http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}/{result_name}")
    if save:
        with open(save, "w") as f:
            f.write(res.text)
    else:
        print(res.json()['res'])


if __name__ == '__main__':
    main(prog_name='asd')