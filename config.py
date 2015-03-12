import os.path as path
from omniv import api as omniv_api

base_dir = path.abspath(path.dirname(__file__))

saves = {
    'ext': '.json',
    'dir': base_dir + '/saves'
}


