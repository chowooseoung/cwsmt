VERSION = [1, 0, 0]


from pkgutil import extend_path
import sys

__path__ = extend_path(__path__, __name__)

def initialize():
    pass

def about():
    pass

def reload_module(name="cwsmt", *args):
    for mod in sys.modules.keys():
        if mod.startswith(name):
            del sys.modules[mod]
