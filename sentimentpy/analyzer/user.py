__author__ = 'dzlab'

from sentimentpy.cleaner import Cleaner
from sentimentpy.io.writer import BufferedWriter
from analyzer import *
from time import time
import logging


class UserAnalyzer(Analyzer):
    logger = logging.getLogger('UserAnalyzer')

    def __init__(self, cleaner=None):
        if not cleaner:
            cleaner = Cleaner()
        self.cleaner = cleaner
        self.names_by_id = {}
        self.texts_by_id = {}

    def analyze(self, comment):
        # ignore non english messages
        """if comment.message.startswith("u'"):
            message = unicode(comment.message)
            return"""
        # process the comment's message
        words = self.cleaner.clean(comment.message)
        text = ' '.join(words)
        if not comment.user_id in self.names_by_id:
            self.names_by_id[comment.user_id] = comment.user_name
            self.texts_by_id[comment.user_id] = text
        else:
            self.texts_by_id[comment.user_id] += ' ' + text

    def finalize(self):
        start_time = time()
        writer = BufferedWriter(filename='messages.csv')
        writer.header('user_id, user_name, texts')
        for uid in self.names_by_id:
            line = uid + ', ' + self.names_by_id[uid] + ', ' + self.texts_by_id[uid].encode("utf-8")
            writer.append(line)
        writer.close()
        end_time = time()
        self.logger.info('Finalization took %s seconds' % str(end_time - start_time))