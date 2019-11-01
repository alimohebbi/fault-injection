import ConfigParser
import os
import os.path


class Config(object):
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.config = ConfigParser.RawConfigParser()
        self.config.read(dir_path + '/config.ini')
