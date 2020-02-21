import types
import pathlib
from os.path import dirname, isfile, join

import glob
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
for module_name, module in modules.items():
    for el in dir(module):
        if el.endswith("Parser"):
            obj = module.__dict__[el]()
            parser_list[module_name] = obj
        if el.startswith("parse"):
            parser_list[module_name] = module.__dict__[el]

snapshot_fields = list(_parser.field for _parser in parser_list.values())
