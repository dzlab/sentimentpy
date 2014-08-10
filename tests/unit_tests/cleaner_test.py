from unittest import TestCase
from sentimentpy.cleaner import Cleaner
from nose.tools import *

class CleanerTest(TestCase):
   class FakeStopWords:
      
      def __init__(self, stop_words=''):
         self.stop_words = stop_words
      def read(self):
         return self.stop_words

   def create_cleaner_with_stopwords(self, words_string):
      return Cleaner(CleanerTest.FakeStopWords(words_string))

   def it_should_remove_stopwords_test(self):
      cleaner = self.create_cleaner_with_stopwords('a')
      cleaned_words = cleaner.remove_stop_words(["a", "sheep"])    
      eq_(cleaned_words, ["sheep"])
   
