__author__ = 'dzlab'

import os
import logging
from logging.handlers import RotatingFileHandler

class LoggerBuilder:
    """A helper class for configuring the logger"""
    def __init__(self):
        self.log = logging.getLogger()
        #logging.basicConfig(level=logging.DEBUG)
        self.log.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    def log_to_file(self, filename=None):
        """create a handler for storing logs on disk"""
        if not filename:
            filename = '%s/../../output/sentimentpy.log' % os.path.dirname(os.path.realpath(__file__))
        file_handler = RotatingFileHandler(filename, 'a', 1000000, 1)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(self.formatter)
        self.log.addHandler(file_handler)
        return self

    def log_to_console(self):
        """create a handler for forwarding logs to console"""
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(self.formatter)
        self.log.addHandler(stream_handler)
        return self

    def build(self):
        return self.log