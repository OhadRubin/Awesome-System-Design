from flask import Flask, render_template, request,make_response,jsonify, url_for
import requests
import click
import time
import random
import pathlib 
import os
from datetime import datetime as dt
# from datetime import 
import datetime
import timeago


@click.group()
# @click.version_option(asd.version)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    pass
    # log.quiet = quiet
    # log.traceback = traceback



def get_bar(count):
    count = count*100
    # The ASCII block elements come in chunks of 8, so we work out how
    # many fractions of 8 we need.
    # https://en.wikipedia.org/wiki/Block_Elements
    bar_chunks, remainder = divmod(int(count * 8 / 4), 8)
    # print(count)
    # First draw the full width chunks
    bar = '█' * bar_chunks

    # Then add the fractional part.  The Unicode code points for
    # block elements are (8/8), (7/8), (6/8), ... , so we need to
    # work backwards.
    if remainder > 0:
        bar += chr(ord('█') + (8 - remainder))

    # If the bar is empty, add a left one-eighth block
    bar = bar or  '▏'
    return bar



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
            snapshot['timestamp'] = timeago.format(dt.fromtimestamp(int(snapshot['timestamp'])/1000))
            for result_name in  snapshot['parsers']:
                res = requests.get(f"http://{_api_host}:{_api_port}/users/{user_id}/snapshots/{snapshot['snapshot_id']}/{result_name}").json()['res']
                if 'path' in res:
                    res['path'] = url_for('static',filename=res['path'])
                if result_name == 'feelings':
                    for fe in ["hunger","thirst","exhaustion","happiness"]:
                        res[fe] = get_bar(res[fe])

                # print(res)
                
                snapshot[result_name]=res

        return make_response(jsonify(snapshots_list), 200)


    @app.route('/users/<int:user_id>',methods = ['GET'])
    def single_user(user_id):
        user = requests.get(f"http://{_api_host}:{_api_port}/users/{user_id}").json()['res']
        # time.gmtime(699746400)
        # datetime.date.fromtimestamp(699746400)
        
        # timeago.format(datetime.date.fromtimestamp(699746400))
        user['birthday'] = str(datetime.date.today().year-datetime.date.fromtimestamp(int(user['birthday'])).year)
        user['gender'] = 'Male' if user['gender']=='0' else 'Female'
        # age =  
        return render_template('single_user.html',user=user)

    

    @app.route('/',methods = ['GET'])
    def users():
        users = requests.get(f"http://{_api_host}:{_api_port}/users").json()['res']
        for user in users:
            user['birthday'] = str(datetime.date.today().year-datetime.date.fromtimestamp(int(user['birthday'])).year)
            user['gender'] = 'Male' if user['gender']=='0' else 'Female'
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
