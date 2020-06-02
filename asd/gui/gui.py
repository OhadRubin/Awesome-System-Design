from flask import Flask, render_template, request,make_response,jsonify, url_for
import requests
import click
import time
import random
import pathlib 
import os

@click.group()
# @click.version_option(asd.version)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    pass
    # log.quiet = quiet
    # log.traceback = traceback







def run_server(host, port, api_host,api_port):
    _api_host= api_host
    _api_port = api_port
    app = Flask(__name__)

    # @app.route('/uploads/<path:filename>')
    # def download_file(filename):
        # return send_from_directory("..data",
                                # filename, as_attachment=True)


    @app.route('/users/<int:user_id>/<int:page_number>',methods = ['GET'])
    def single_user_p(user_id,page_number=0):
        snapshots = requests.get(f"http://{_api_host}:{_api_port}/users/{user_id}/snapshots_p/{page_number}").json()['res']
        snapshots_list = []

        for snapshot in snapshots:
            res = requests.get(f"http://{_api_host}:{_api_port}/users/{user_id}/snapshots/{snapshot['snapshot_id']}").json()['res']
            snapshots_list.append(res)

        for snapshot in snapshots_list:
            for result_name in  snapshot['parsers']:
                res = requests.get(f"http://{_api_host}:{_api_port}/users/{user_id}/snapshots/{snapshot['snapshot_id']}/{result_name}").json()['res']
                if 'path' in res:
                    # print()
                    # app.send_static_file("../"+res['path'])
                    res['path'] = url_for('static',filename=res['path'])
                    print(res['path'])
                snapshot[result_name]=res

        return make_response(jsonify(snapshots_list), 200)


    @app.route('/users/<int:user_id>',methods = ['GET'])
    def single_user(user_id):
        user = requests.get(f"http://{_api_host}:{_api_port}/users/{user_id}").json()['res']
        return render_template('single_user.html',user=user)

    

    @app.route('/',methods = ['GET'])
    def users():
        users = requests.get(f"http://{_api_host}:{_api_port}/users").json()['res']
        return render_template('all_users.html',users=users)
    app.run(host=host,port=port,debug=True)

@main.command('run-server')
@click.option('-h', '--host', default='0.0.0.0')
@click.option('-p', '--port', default=8080)
@click.option('-H', '--api_host', default='127.0.0.1')
@click.option('-P', '--api_port', default=5000)
def run_server_cli(host, port, api_host,api_port):
    # sh.bash(cmd)
    try:
        os.remove(pathlib.Path.cwd()/"asd/gui/static/data")
    except:
        pass
    try:
        os.symlink(pathlib.Path("data").absolute(),pathlib.Path.cwd()/"asd/gui/static/data") 
    except:
        pass

    run_server(host,port, api_host,api_port)
    

if __name__ == '__main__':
    main(prog_name='asd')
