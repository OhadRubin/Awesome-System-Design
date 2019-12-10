from datetime import datetime
from functools import wraps
from http.server import *
from pathlib import Path
import re
import socket
import struct
import sys
import threading
import time
from .website import Website


website = Website()

_INDEX_HTML = '''
<html>
    <title>Brain Computer Interface</title>

    <body>
        <ul>
            {users}
        </ul>
    </body>
</html>
'''
_USER_LINE_HTML = '''
<li><a href="/users/{user_id}">user {user_id}</a></li>
'''

_USER_HTML = """<html>
    <head>
        <title>Brain Computer Interface: User {user_id}</title>
    </head>
    <body>
        <table>
            {thoughts}
        </table>
    </body>
</html>"""

_THOUGHT_LINE_HTML = """<tr><td>{timestamp}</td><td>{thought_data}</td></tr>"""
# def sanitize_timestamp()
@website.route('/users/([0-9]+)')
def write_user(user_id):
    user_dir = Path(website.data_dir) / user_id
    thought_html = []
    for thought_file in user_dir.iterdir():
        with thought_file.open() as file:
            for line in file:
                timestamp = thought_file.name[:-3].split("_")
                timestamp = " ".join([timestamp[0],timestamp[1].replace("-",":")])
                thought_html.append(_THOUGHT_LINE_HTML.format(timestamp=timestamp,thought_data=line))
    data = _USER_HTML.format(user_id=user_id,thoughts='\n'.join(thought_html))
    return 200,data

@website.route('/')
def write_index():
    data_dir = Path(website.data_dir)
    users_html = []
    for user_dir in data_dir.iterdir():
        users_html.append(_USER_LINE_HTML.format(user_id=user_dir.name))
    data = _INDEX_HTML.format(users='\n'.join(users_html))
    return 200,data


def run_webserver(address,data_dir):
    website.data_dir = data_dir
    website.run(address)

def main(argv):
    if len(argv) != 3:
        print(f'USAGE: {argv[0]} <address> <data_dir>' )
        return 1
    try:
        address = tuple(argv[1].split(":"))
        address = (address[0],int(address[1]))
        
        run_webserver(address,argv[2])
        
    except KeyboardInterrupt:
        return 0
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))


