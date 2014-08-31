from __future__ import division
__author__ = 'dzlab'

from analyzer import *
from sentimentpy.cleaner import *
from sentimentpy.helper import WatchTime
from sentimentpy.io.writer import BufferedWriter
from guess_language import guess_language
import logging
import os
import numpy


class SentimentAnalyzer(Analyzer):
    logger = logging.getLogger('SentimentAnalyzer')
    POSITIVE_FILE = '%s/../../data/%s' % (os.path.dirname(os.path.realpath(__file__)), 'positive.txt')
    NEGATIVE_FILE = '%s/../../data/%s' % (os.path.dirname(os.path.realpath(__file__)), 'negative.txt')

    def __init__(self, cleaner=None):
        if not cleaner:
            self.cleaner = CleanerComposer()
            self.cleaner.normalize().replace_special_characters().remove_punctuations().split().remove_meaningless_words()
        else:
            self.cleaner = cleaner
        positive_words = open(self.POSITIVE_FILE, 'r')
        self.positives = positive_words.read().split('\n')
        positive_words.close()
        negative_words = open(self.NEGATIVE_FILE, 'r')
        self.negatives = negative_words.read().split('\n')
        negative_words.close()
        self.scores = self.freq_mat = numpy.zeros(20, int)
        self.watch = WatchTime()

    def analyze(self, comment):
        self.watch.start()
        if not comment.language:
            comment.language = guess_language(comment.message)
        if not comment.language == 'en':
            return
        words = self.cleaner.clean(comment.message)
        positive_count = 0
        negative_count = 0
        for w in words:
            if w in self.positives:
                positive_count += 1
            elif w in self.negatives:
                negative_count += 1
        score = (positive_count - negative_count) / len(words)
        index = round(score * 10 + 10)
        self.scores[index] += 1
        self.watch.stop()

    def finalize(self):
        self.logger.info('Analyzing the comments took %s seconds' % str(self.watch.total()))
        self.watch.reset()
        # start a new watch
        self.watch.start()
        writer = BufferedWriter(filename='data.tsv')
        writer.header('range' + '\t' + 'frequency')
        for i in range(0, len(self.scores)):
            writer.append(str(i-10) + '\t' + str(self.scores[i]))
        writer.close()
        self.watch.stop()
        self.logger.info('Finalization took %s seconds' % str(self.watch.total()))