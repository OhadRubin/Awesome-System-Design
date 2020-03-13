from functools import wraps
from http.server import *
import socket
import time
import sys
import struct
from datetime import datetime
import threading
from pathlib import Path
import re


class Website:
    def __init__(self):
        self.handler_dict = {}

    def route(self, path):
        def decorator(f):
            self.handler_dict[path] = f

            @wraps(f)
            def wrapper(*args, **kwargs):
                return f(*args, **kwargs)

            return wrapper

        return decorator

    def run(self, address):
        ws = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                if ws.handler_dict.get(self.path):
                    handler_func = ws.handler_dict[self.path]
                    status_code, data = handler_func()
                else:
                    for key in ws.handler_dict.keys():
                        res = re.fullmatch(key, self.path)
                        if res:
                            handler_func = ws.handler_dict[key]
                            status_code, data = handler_func(*res.groups())
                            break
                    else:
                        status_code, data = 404, ''
                self.send_response(status_code)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Content-Length', len(data))
                self.end_headers()
                self.wfile.write(data.encode("utf-8"))

        httpd = HTTPServer(address, Handler)
        httpd.serve_forever()
