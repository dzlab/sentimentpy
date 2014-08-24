#!/usr/bin/env python

"""
A collection of methods for pre-processing comments text
"""

import os
import string
import re
import logging
from porter_stemmer import PorterStemmer


class Cleaner:
    STOP_WORDS_FILE = '%s/../data/english.stop' % os.path.dirname(os.path.realpath(__file__))
    logger = logging.getLogger('Cleaner')
    stopwords = []

    LINK = re.compile(r'(?:(http://)|(www\.))(\S+\b/?)([!"#$%&\'()*+,\-./:;<=>?@[\\\]^_`{|}~]*)(\s|$)', re.I)
    ATUSER = re.compile(r'@[a-zA-Z0-9]+', re.I)
    HASHTAG = re.compile(r'#[a-zA-Z0-9]+', re.I)
    SMILEY = re.compile(r'^(:\(|:\))+$', re.I) # matches only :) and :(
    WORD = re.compile(r'[a-zA-Z][a-zA-Z0-9]*', re.I)
    PUNCTUATION = re.compile('[%s]' % re.escape(string.punctuation))

    def __init__(self, stopwords_io_stream=None):
        self.stemmer = PorterStemmer()

        if not stopwords_io_stream:
            stopwords_io_stream = open(Cleaner.STOP_WORDS_FILE, 'r')

        self.stopwords = stopwords_io_stream.read().split()

    def clean(self, message):
        """Remove any nasty nasty grammar token from a message"""
        message = self.normalize(message)
        message = self.replace_special_characters(message)
        message = self.remove_punctuations(message)
        words = message.split()
        words = self.remove_meaningless_words(words)
        words = self.tokenize(words)
        words = self.remove_stop_words(words)
        return words

    def normalize(self, message):
        message = message.replace('\n', ' ')
        return message.lower()
   
    def replace_special_characters(self, message):
        """Replace website urls with the string 'url', @user with at_user"""
        message = Cleaner.LINK.sub('url', message)
        message = Cleaner.ATUSER.sub('at_user', message)
        message = Cleaner.HASHTAG.sub(self._remove_hashtag, message)
        return message

    #@staticmethod
    def _remove_hashtag(self, match):
        """Remove '#' from the hashtag """
        groups = match.groups()
        if len(groups) == 0:
            return None
        user = groups[0].replace('#', '')
        return user

    def remove_punctuations(self, message):
        """Remove punctuations using very fast string.translate() method"""
        #table = string.maketrans(string.punctuation, " " * len(string.punctuation))
        #message = message.translate(table, string.punctuation)
        message = Cleaner.PUNCTUATION.sub(' ', message)
        message = message.strip()
        return message

    def remove_stop_words(self, words):
        """ Filter words from low value ones such 'the', 'is' and 'on'.
        words -- the list of words from whish stop words will be removed
        """
        return [word for word in words if word not in self.stopwords ]

    def remove_meaningless_words(self, words):
        return [word for word in words if Cleaner.WORD.match(word)]

    def tokenize(self, words):
        """"""
        self.stemmer = PorterStemmer()
        return [self.stemmer.stem(word, 0, len(word)-1) for word in words]

