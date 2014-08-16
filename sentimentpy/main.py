from analyzer.length import LengthAnalyzer
from analyzer.language import LanguageAnalyzer
from helper import *
import logging
from time import time

FILENAME = '6815841748_10152075477696749.txt'
COMMENTS_FILE = '%s/../data/%s' % (os.path.dirname(os.path.realpath(__file__)), FILENAME)

logger = logging.getLogger()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    start_time = time()
    analyzers = []
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
