#!/usr/bin/env python

from analyze import AnalyzerManager
from inout.mongodb import MongoWorkerPool, MongoDb
from helper import *
from model import Comment
from core.analyzer.language import LanguageAnalyzer
from core.analyzer.length import LengthAnalyzer
from core.analyzer.sentiment import SentimentAnalyzer
from core.analyzer.user import UserAnalyzer
from inout.reader import *
from utils.logs import LoggerBuilder
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
        self.op.add_option("-p",
                           dest="process",
                           default=False,
                           help="Process the stored comments")

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
        """Handle the options submit to this program"""
        (opts, args) = self.op.parse_args()
        logger.debug("Handling options %s" % opts)
        if len(args) != 0:
            logger.info("Program called with %s" % args)
            self.op.error("This script should take no arguments.")
            sys.exit(1)

        if not (opts.directory or opts.file) and not opts.process:
            self.op.print_help()
            return None

        result = []
        if opts.directory:
            result = OptionsHandler.scan(opts.directory)
        if opts.file:
            result.append(opts.file)
        self.handle_storage(result)
        if opts.process:
            self.handle_analysis()

    def handle_storage(self, files):
        if not files or len(files) == 0:
            logger.info("No file to analyze is provided!")
            #sys.exit(0)
            return
        logger.info("Starting the processing of comments files")
        loader = CommentsLoader().load(files).close()

    def handle_analysis(self):
        logger.info("Starting the analysis of stored comments")
        watch = WatchTime()
        watch.start()
        db = MongoDb()
        # create an analysis manager and register the analyzers
        analyzer = AnalyzerManager(db=db)
        analyzer.register(LengthAnalyzer())
        analyzer.register(LanguageAnalyzer())
        analyzer.register(UserAnalyzer())
        analyzer.register(SentimentAnalyzer())
        comments = db.comments.find()
        i = 0
        for item in comments:
            i += 1
            comment = Comment.from_dict(**item)
            analyzer.process(comment)
        analyzer.finalize()
        db.close()
        watch.stop()
        logger.info('Done in %s seconds' % str(watch.total()))


class CommentsLoader:
    logger = logging.getLogger('CommentsLoader')

    def __init__(self):
        self.pool = MongoWorkerPool(10)
        self.analyzers = []

    def load(self, files):
        """Load the content of a list of files into the database"""
        for item in files:
            self.logger.debug("Parsing data from %s" % item)
            reader = Reader(filename=item, parse=False)
            while True:
                comment = reader.next()
                if not comment:
                    break
                # enqueue the comment for storage
                self.pool.add_comment(comment)
                # enqueue the comment for analysis

            reader.close()
        return self

    def close(self):
        """Wait for all comments to be stored then close pool connections"""
        self.pool.wait_completion()
        self.pool.close()
        return self


#e.g. python main.py -f /home/dzlab/Work/sentimentpy/data/6815841748_10152075477696749.txt
if __name__ == '__main__':
    #sys.settrace(trace_calls)
    logger = LoggerBuilder().log_to_file().log_to_console().build()
    OptionsHandler().handle_options()

