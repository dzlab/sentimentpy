__author__ = 'dzlab'

import sys
import logging
from threading import Thread
from Queue import Queue
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

DATABASE = "sentimentdb"


class MongoDb:
    """MongoDB client wrapper"""
    logger = logging.getLogger('MongoDb')

    def __init__(self):
        try:
            self.connection = MongoClient(host="localhost", port=27017)
        except ConnectionFailure, e:
            MongoDb.logger.info("Could not connect to MongoDB: %s" % e)
            sys.exit(1)
        self.sentimentdb = self.connection.sentimentdb
        self.comments = self.connection.sentimentdb.comments
        MongoDb.logger.debug("Successfully opened connection to the comments '%s'" % DATABASE)

    def close(self):
        self.connection.close()
        MongoDb.logger.debug("Successfully closed connection to '%s'" % DATABASE)


class MongoWorker(Thread):
    """Thread executing inserts to mongodb from a given comments queue"""
    logger = logging.getLogger('MongoWorker')

    def __init__(self, comments_queue):
        Thread.__init__(self)
        self.comments_queue = comments_queue
        self.daemon = True
        try:
            self.connection = MongoClient(host="localhost", port=27017)
        except ConnectionFailure, e:
            MongoWorker.logger.info("Could not connect to MongoDB: '%s'" % DATABASE)
            sys.exit(1)
        self.comments_collection = self.connection.sentimentdb.comments
        MongoWorker.logger.debug("%s successfully opened connection to the comments '%s'" % (self.name, DATABASE))
        self.start()

    def run(self):
        while True:
            comment = self.comments_queue.get()
            self.comments_collection.insert(comment.to_dict())
            self.comments_queue.task_done()

    def close(self):
        self.connection.close()
        MongoWorker.logger.debug("%s successfully closed connection to '%s'" % (self.name, DATABASE))


class MongoWorkerPool:
    """Pool of connections to mongodb for a queue"""
    logger = logging.getLogger('MongoWorkerPool')

    def __init__(self, size):
        self.logger.debug("Initiating a pool of %s MongoWorker(s)" % size)
        self.comments = Queue(size)
        self.workers = []
        for _ in range(size):
            worker = MongoWorker(self.comments)
            self.workers.append(worker)

    def add_comment(self, comment):
        """Add a comment to the queue"""
        self.comments.put(comment)

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.comments.join()

    def close(self):
        self.logger.debug("Closing all workers in the pool")
        for worker in self.workers:
            worker.close()