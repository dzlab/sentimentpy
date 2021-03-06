from __future__ import division
__author__ = 'dzlab'

from core.analyzer import Analyzer
from core.cleaner import *
from core.helper import WatchTime, guess_language_thread_safe
from core.inout.writer import BufferedWriter
import logging
import os
import numpy


class SentimentAnalyzer(Analyzer):
    """Estimates the frequency of each sentiment score between -10 and +10 of all messages"""
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

    def name(self):
        return 'sentiment'

    def analyze(self, comment):
        self.watch.start()
        if not comment.language:
            comment.set_language(guess_language_thread_safe(comment.message))
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
        if index == len(self.scores):
            index -= 1
        self.scores[index] += 1
        self.watch.stop()

    def finalize(self, output=None, close=True):
        self.logger.info('Analyzing the comments took %s seconds' % str(self.watch.total()))
        self.watch.reset()
        # start a new watch
        self.watch.start()
        if not output:
            output = BufferedWriter(filename='data.tsv', file_format='tsv')
        output.header(['range', 'frequency'])
        for i in range(0, len(self.scores)):
            data = {'range': i-10, 'frequency': self.scores[i]}
            output.append(data)
        if close:
            output.close()
        self.watch.stop()
        self.logger.info('Finalization took %s seconds' % str(self.watch.total()))