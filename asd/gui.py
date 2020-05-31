from flask import Flask, render_template, request
import requests
app = Flask(__name__)
host = ''
port = ''


@app.route('/users/<int:user_id>',methods = ['GET'])
def single_user(user_id):
    user = requests.get(f"http://{host}:{port}/users/{user_id}").json()['res']
    snapshots = requests.get(f"http://{host}:{port}/users/{user_id}/snapshots").json()['res']
    snapshots = snapshots[:10]
    snapshots_list = []

    for snapshot in snapshots:
        res = requests.get(f"http://{host}:{port}/users/{user_id}/snapshots/{snapshot['snapshot_id']}").json()['res']
        snapshots_list.append(res)
        # print(res)
        # pass
    for snapshot in snapshots_list:
        for result_name in  snapshot['parsers']:
            res = requests.get(f"http://{host}:{port}/users/{user_id}/snapshots/{snapshot['snapshot_id']}/{result_name}").json()['res']
            snapshot[result_name]=res
            # res = res

        # pass
    # print(snapshots_list)
    return render_template('single_user.html',user=user,snapshots=snapshots_list)

@app.route('/users/<int:user_id>/<int:page_number>',methods = ['GET'])
def single_user_p(user_id,page_number):
    user = requests.get(f"http://{host}:{port}/users/{user_id}").json()['res']
    snapshots = requests.get(f"http://{host}:{port}/users/{user_id}/snapshots_p/{page_number}").json()['res']
    snapshots = snapshots
    snapshots_list = []

    for snapshot in snapshots:
        res = requests.get(f"http://{host}:{port}/users/{user_id}/snapshots/{snapshot['snapshot_id']}").json()['res']
        snapshots_list.append(res)
        # print(res)
        # pass
    for snapshot in snapshots_list:
        for result_name in  snapshot['parsers']:
            res = requests.get(f"http://{host}:{port}/users/{user_id}/snapshots/{snapshot['snapshot_id']}/{result_name}").json()['res']
            snapshot[result_name]=res
            # res = res

        # pass
    # print(snapshots_list)
    return render_template('single_user.html',user=user,snapshots=snapshots_list)


@app.route('/',methods = ['GET'])
def users():
    users = requests.get(f"http://{host}:{port}/users").json()['res']
    return render_template('all_users.html',users=users)

if __name__ == '__main__':
    host= '127.0.0.1'
    port = 5000
    app.run(host='0.0.0.0',port=6969,debug=True)