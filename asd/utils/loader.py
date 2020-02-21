import types
import pathlib
def load(path):
    mod_name = pathlib.Path(path).name[:-3]
    module = types.ModuleType(mod_name)
    with open(path) as f:
        module_str = f.read()
    exec(module_str, module.__dict__)
    return module