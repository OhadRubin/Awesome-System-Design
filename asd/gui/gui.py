from flask import Flask, render_template, request,make_response,jsonify, url_for
import requests
app = Flask(__name__)
import time
import random
host = ''
port = ''
heading = "Lorem ipsum dolor sit amet."

content = """
Lorem ipsum dolor sit amet consectetur, adipisicing elit. 
Repellat inventore assumenda laboriosam, 
obcaecati saepe pariatur atque est? Quam, molestias nisi.
"""



@app.route('/users/<int:user_id>/<int:page_number>',methods = ['GET'])
def single_user_p(user_id,page_number=0):
    snapshots = requests.get(f"http://{host}:{port}/users/{user_id}/snapshots_p/{page_number}").json()['res']
    snapshots_list = []

    for snapshot in snapshots:
        res = requests.get(f"http://{host}:{port}/users/{user_id}/snapshots/{snapshot['snapshot_id']}").json()['res']
        snapshots_list.append(res)
        # print(res)
        # pass
    for snapshot in snapshots_list:
        for result_name in  snapshot['parsers']:
            res = requests.get(f"http://{host}:{port}/users/{user_id}/snapshots/{snapshot['snapshot_id']}/{result_name}").json()['res']
            if 'path' in res:
                res['path'] = url_for('static',filename=res['path'])
            snapshot[result_name]=res

    return make_response(jsonify(snapshots_list), 200)


@app.route('/users/<int:user_id>',methods = ['GET'])
def single_user(user_id):
    user = requests.get(f"http://{host}:{port}/users/{user_id}").json()['res']
    return render_template('single_user.html',user=user)

 

@app.route('/',methods = ['GET'])
def users():
    users = requests.get(f"http://{host}:{port}/users").json()['res']
    return render_template('all_users.html',users=users)

if __name__ == '__main__':
    host= '127.0.0.1'
    port = 5000
    app.run(host='0.0.0.0',port=6969,debug=True)