import os
import logging
from logging.handlers import RotatingFileHandler
from time import time

class Comment:
    """a class representation of a comment"""
    def __init__(self):
        self.id = None
        self.user_id = None
        self.user_name = None
        self.message = None
        self.created_time = None
        self.like_count = 0


class WatchTime:
    def __init__(self):
        self.start_time = 0
        self.stop_time = 0
        self.total_time = 0

    def start(self):
        self.start_time = time()
        self.stop_time = self.start_time

    def stop(self):
        self.stop_time = time()
        self.total_time += (self.stop_time - self.start_time)

    def elapsed(self):
        return self.stop_time - self.start_time

    def total(self):
        return self.total_time

def get_logger():
    my_logger = logging.getLogger()
    #logging.basicConfig(level=logging.DEBUG)
    my_logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    # create a handler for storing logs on disk
    logs_file = '%s/../output/sentimentpy.log' % os.path.dirname(os.path.realpath(__file__))
    file_handler = RotatingFileHandler(logs_file, 'a', 1000000, 1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    my_logger.addHandler(file_handler)
    # create a handler for forwarding logs to console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    my_logger.addHandler(stream_handler)
    return my_logger

