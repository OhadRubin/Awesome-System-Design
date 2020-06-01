import types
import pathlib
from os.path import dirname, isfile, join
import asd.utils.asd_pb2 as asd_pb2
import os
from asd.utils import mq
import glob
import json


modules = {}
modules_list = glob.glob(join(dirname(__file__), "*.py"))
for path in modules_list:
    if isfile(path) and not path.endswith('__init__.py') and not path.endswith('__main__.py'):
        mod_name = pathlib.Path(path).name[:-3]
        module = types.ModuleType(mod_name)
        with open(path) as f:
            module_str = f.read()
        exec(module_str, module.__dict__)
        modules[mod_name] = module

parser_list = {}
snapshot_fields = set()
for module_name, module in modules.items():
    for el in dir(module):
        if el.endswith("Parser"):
            obj = module.__dict__[el]()
            parser_list[module_name] = obj.parse
            snapshot_fields.add(obj.field)
        if el.startswith("parse"):
            parser_list[module_name] = module.__dict__[el]
            snapshot_fields.add(module.__dict__[el].field)

snapshot_fields = list(snapshot_fields)


class Context:
    def __init__(self, user_id, timestamp):
        self.user_id = user_id
        self.timestamp = timestamp

    def path(self, filename):
        # print(self.timestamp)
        os.makedirs(f"data/{self.user_id}/{self.timestamp}", exist_ok=True)
        return f"data/{self.user_id}/{self.timestamp}/{filename}"

    def save(self, filename, data):
        filename = self.path(filename)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            f.write(data)


def run_parser(parser_name, packet):
    parse_method = parser_list[parser_name]

    packet = asd_pb2.Packet.FromString(packet)
    context = Context(user_id=packet.user.user_id, timestamp=packet.snapshot.datetime)
    res = parse_method(context=context, snapshot=packet.snapshot)
    user = dict(username=packet.user.username, user_id=packet.user.user_id,
                gender=packet.user.gender, birthday=packet.user.birthday)

    return json.dumps({"parser_name": parser_name, "data": {"user": user,
                                                            "timestamp": packet.snapshot.datetime,
                                                            "result": res}})


def parse(parser_name, path):
    assert isinstance(path, str) and path.endswith(".raw")
    with open(path, "rb") as x:
        return run_parser(parser_name, packet=x.read())

