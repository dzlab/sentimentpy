#!/usr/bin/env python

"""
A collection of methods for pre-processing comments text
"""

import os, string, re
from porter_stemmer import PorterStemmer

class Cleaner:
   STOP_WORDS_FILE = '%s/../data/english.stop' % os.path.dirname(os.path.realpath(__file__))
   
   stemmer = None
   stopwords = []

   link = re.compile(r'(?:(http://)|(www\.))(\S+\b/?)([!"#$%&\'()*+,\-./:;<=>?@[\\\]^_`{|}~]*)(\s|$)', re.I)
   at_user = re.compile(r'@[a-zA-Z0-9]+', re.I)
   hashtag = re.compile(r'#[a-zA-Z0-9]+', re.I)

   def __init__(self, stopwords_io_stream = None):
      self.stemmer = PorterStemmer()

      if(not stopwords_io_stream):
         stopwords_io_stream = open(Cleaner.STOP_WORDS_FILE, 'r')

      self.stopwords = stopwords_io_stream.read().split()

   def clean(self, message):
      """Remove any nasty nasty grammar token from a message"""
      message = self.lowercase(message)
      message = self.replace_special_characters(message)
      message = self.remove_punctuations(message)
      words = message.split()
      words = self.tokenize(words)
      words = self.remove_stop_words(words)
      return words

   def lowercase(self, message):
      return message.lower()
   
   def replace_special_characters(self, message):
      """Replace website urls with the string 'url', @user with at_user"""
      message = link.sub('url', message)
      message = at_user.sub('at_user', message)
      message = hashtag.sub(_remove_hashtag, message)
      return message

   def _remove_hashtag(match):
      """Remove '#' from the hashtag """
      groups = match.groups()
      user = groups[0].replace('#', '')
      return user

   def remove_punctuations(self, message):
      """Remove punctuations using very fast string.translate() method"""
      table = string.maketrans("", "")
      message = message.translate(table, string.punctuation)
      return message

   def remove_stop_words(self, words):
      """ Filter words from low value ones such 'the', 'is' and 'on'.
      words -- the list of words from whish stop words will be removed 
      """
      return [ word for word in words if word not in self.stopwords ]

   def tokenize(self, words):
      """"""
      stemmer = PorterStemmer()
      return [stemmer.stem(word, 0, len(word)-1) for word in words]

