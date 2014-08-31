from __future__ import division
__author__ = 'dzlab'

import re
import string
import math


class StringUtils:
    PUNCTUATION = re.compile('[%s\s]' % re.escape(string.punctuation))

    def __init__(self):
        return

    @staticmethod
    def word_frequency(text):
        """Calculates the word frequencies in a given text"""
        words = StringUtils.PUNCTUATION.sub(' ', text).split()
        words_freq = {}
        # calculate word's count
        for w in words:
            if not w in words_freq:
                words_freq[w] = 1
            else:
                words_freq[w] += 1
        # normalize the counts into frequencies
        text_size = len(words)
        for w in words_freq:
            words_freq[w] /= text_size
        return words_freq

    @staticmethod
    def words_distance(w1, w2):
        """Measure the distance between two vectors of words with their frequencies"""
        if w1 is w2:
            return 0
        dist = 0
        visited = []
        for w in w1:
            visited.append(w)
            if w in w2:
                dist += math.pow(w1[w] - w2[w], 2)
            else:
                dist += math.pow(w1[w], 2)
        # look for the remaining words in w2 (which are not in w1)
        for w in w2:
            if not w in w1:
                dist += math.pow(w2[w], 2)
        dist = math.sqrt(dist)
        return dist