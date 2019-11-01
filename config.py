from ConfigParser import RawConfigParser


class Config(object):
    def __init__(self):
        self.config = RawConfigParser()
        self.config.read('config')
