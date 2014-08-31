from analyzer.length import LengthAnalyzer
from analyzer.language import LanguageAnalyzer
from analyzer.user import UserAnalyzer
from helper import *
from io.reader import *

from time import time

FILENAME = '6815841748_10152075477696749.txt'
COMMENTS_FILE = '%s/../data/%s' % (os.path.dirname(os.path.realpath(__file__)), FILENAME)


if __name__ == '__main__':
    logger = get_logger()
    watch = WatchTime()
    watch.start()
    analyzers = [ ]
    #analyzers.append(LengthAnalyzer())
    #analyzers.append(LanguageAnalyzer())
    analyzers.append(UserAnalyzer())
    reader = Reader(filename=COMMENTS_FILE)
    while True:
        comment = reader.next()
        if not comment:
            break
        for analyzer in analyzers:
            analyzer.analyze(comment)
    reader.close()
    for analyzer in analyzers:
        analyzer.finalize()
    watch.stop()
    logger.info('Done in %s seconds' % str(watch.total()))
