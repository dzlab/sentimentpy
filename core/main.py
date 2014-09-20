#!/usr/bin/env python

from analyzer.length import LengthAnalyzer
from analyzer.language import LanguageAnalyzer
from analyzer.user import UserAnalyzer
from analyzer.sentiment import SentimentAnalyzer
from inout.mongodb import MongoWorkerPool
from helper import *
from inout.reader import *
from utils.logs import LoggerBuilder
from time import time
import sys
import os
from optparse import OptionParser

FILENAME = '6815841748_10152075477696749.txt'
COMMENTS_FILE = '%s/../data/%s' % (os.path.dirname(os.path.realpath(__file__)), FILENAME)


class OptionsHandler:
    def __init__(self):
        self.op = OptionParser()
        self.op.add_option("-f",
                           dest="file",
                           type="string",
                           help="Load data from this file")
        self.op.add_option("-d",
                           dest="directory",
                           type="string",
                           help="Scan the directory for data files")

    @staticmethod
    def scan(directory):
        """Scan this directory for data files"""
        logger.info("Scanning %s for data files to parse." % directory)
        result = []
        for item in os.listdir(directory):
            item_full_path = os.path.join(directory, item)
            if os.path.isdir(item_full_path):
                sub_items = OptionsHandler.scan(item_full_path)
                result.extend(sub_items)
            else:
                logger.debug("Found data file: %s" % item_full_path)
                result.append(item_full_path)
        return result

    def handle_options(self):
        (opts, args) = self.op.parse_args()
        logger.debug("Handling options %s" % opts)
        if len(args) != 0:
            logger.info("Program called with %s" % args)
            self.op.error("This script should take no arguments.")
            sys.exit(1)

        if not opts.directory and not opts.file:
            self.op.print_help()
            return None

        result = []
        if opts.directory:
            result = OptionsHandler.scan(opts.directory)
        if opts.file:
            result.append(opts.file)
        return result


class CommentsLoader:
    logger = logging.getLogger('CommentsLoader')

    def __init__(self):
        self.pool = MongoWorkerPool(10)
        self.analyzers = []

    def register(self, analyzer):
        #analyzers.append(LengthAnalyzer())
        #analyzers.append(LanguageAnalyzer())
        #analyzers.append(UserAnalyzer())
        #analyzers.append(SentimentAnalyzer())
        self.analyzers.append(analyzer)

    def load(self, files):
        """Load the content of a list of files into the database"""
        for item in files:
            self.logger.debug("Parsing data from %s" % item)
            reader = Reader(filename=item)
            while True:
                comment = reader.next()
                if not comment:
                    break

                self.pool.add_comment(comment)
            reader.close()
        return self

    def close(self):
        """Wait for all comments to be stored then close pool connections"""
        self.pool.wait_completion()
        self.pool.close()
        return self


def do_analyze():
    #e.g. python main.py -f /home/dzlab/Work/sentimentpy/data/6815841748_10152075477696749.txt
    watch = WatchTime()
    watch.start()
    analyzers = []
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


if __name__ == '__main__':
    logger = LoggerBuilder().log_to_file().log_to_console().build()
    files = OptionsHandler().handle_options()
    if not files or len(files) == 0:
        logger.info("No file to analyze is provided!")
        sys.exit(0)
    loader = CommentsLoader().load(files).close()
