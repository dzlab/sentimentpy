from analyzer.length import LengthAnalyzer
from analyzer.language import LanguageAnalyzer
from helper import *
import logging
from logging.handlers import RotatingFileHandler
from time import time

FILENAME = '6815841748_10152075477696749.txt'
COMMENTS_FILE = '%s/../data/%s' % (os.path.dirname(os.path.realpath(__file__)), FILENAME)


def get_logger():
    my_logger = logging.getLogger()
    #logging.basicConfig(level=logging.DEBUG)
    my_logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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


if __name__ == '__main__':
    logger = get_logger()
    start_time = time()
    analyzers = [ ]
    analyzers.append(LengthAnalyzer())
    analyzers.append(LanguageAnalyzer())
    reader = Reader(COMMENTS_FILE)
    while True:
        comment = reader.next()
        if not comment:
            break
        for analyzer in analyzers:
            analyzer.analyze(comment)
    reader.close()
    for analyzer in analyzers:
        analyzer.finalize()

    end_time = time()
    logger.info('Done in %s seconds' % str(end_time - start_time))
