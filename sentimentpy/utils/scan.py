__author__ = 'dzlab'

import os
import sys
import logging

from optparse import OptionParser
from sentimentpy.io.reader import Reader
from sentimentpy.io.mongodb import MongoWorkerPool

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('scan.py')


def scan(directory):
    """Scan this directory for data files"""
    logger.info("Scanning %s for data files to parse." % directory)
    data_files = []
    for f in os.listdir(directory):
        if os.path.isdir(f):
            data_files.append(scan(f))
        else:
            logger.debug("Found data file: %s" % f)
            data_files.append(f)

    """for root, dirs, files in os.walk(directory):
        for file in files:
            pass
        pass"""
    return data_files


def load(db, data_file):
    logger.debug("Parsing data from %s" % data_file)
    reader = Reader(filename=data_file)
    while True:
        comment = reader.next()
        if not comment:
            break
        db.add_comment(comment)
    reader.close()


def handle_options():
    op = OptionParser()
    op.add_option("-f",
                  dest="file",
                  type="string",
                  help="Load data from this file")
    op.add_option("-d",
                  dest="directory",
                  type="string",
                  help="Scan the directory for data files")

    (opts, args) = op.parse_args()
    if len(args) != 0:
        logger.info("Program called with %s" % args)
        op.error("This script should take no arguments.")
        sys.exit(1)
    """if opts.help:
        print(__doc__)
        op.print_help()
        sys.exit(0)"""
    files = []
    if opts.directory:
        files = scan(opts.directory)
    if opts.file:
        files.append(opts.file)
    return files

if __name__ == '__main__':
    #files = handle_options()
    pool = MongoWorkerPool(10)
    files = ["/home/dzlab/Work/sentimentpy/data/6815841748_10152075477696749.txt"]
    for f in files:
        load(pool, f)
    pool.wait_completion()
    pool.close()
