__author__ = 'dzlab'

import sys
import logging
from sentimentpy.analyze import Analyzer
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class MongoDb(Analyzer):
    logger = logging.getLogger('MongoDb')
    DATABASE = "sentimentdb"

    def __init__(self):
        try:
            self.connection = MongoClient(host="localhost", port=27017)
        except ConnectionFailure, e:
            MongoDb.logger.info("Could not connect to MongoDB: %s" % e)
            sys.exit(1)
        self.comments = self.connection.sentimentdb.comments
        MongoDb.logger.debug("Successfully opened connection to the comments database")

    def analyze(self, comment):
        self.comments.insert(comment.to_dict())

    def finalize(self):
        self.connection.close()
        MongoDb.logger.debug("Successfully closed connection to database")