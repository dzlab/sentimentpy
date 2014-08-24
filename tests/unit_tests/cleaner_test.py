from unittest import TestCase
from sentimentpy.cleaner import Cleaner
from nose.tools import *


class CleanerTest(TestCase):

    class FakeStopWords:
      
        def __init__(self, stop_words=''):
            self.stop_words = stop_words

        def read(self):
            return self.stop_words

    @staticmethod
    def create_cleaner_with_stopwords(words_string=None):
        if not words_string:
            words_string = ''
        return Cleaner(CleanerTest.FakeStopWords(words_string))

    def it_should_remove_stopwords_test(self):
        cleaner = self.create_cleaner_with_stopwords('a')
        cleaned_words = cleaner.remove_stop_words(["a", "sheep"])
        eq_(cleaned_words, ["sheep"])

    def it_should_remove_punctuations_test(self):
        cleaner = self.create_cleaner_with_stopwords()
        cleaned = cleaner.remove_punctuations("Hello world!")
        eq_(cleaned, "Hello world")
        cleaned = cleaner.remove_punctuations("Also CHECK W/SNOPES(MEDICAL/KITHIL)\n\nPLEASE PASS THIS OUTRAGE TO EVERYONE ON YOUR LIST!!!")
        eq_(cleaned, "Also CHECK W SNOPES MEDICAL KITHIL \n\nPLEASE PASS THIS OUTRAGE TO EVERYONE ON YOUR LIST")

    def it_should_not_clean_text_test(self):
        cleaner = self.create_cleaner_with_stopwords()
        cleaned = cleaner.clean("hello")
        eq_(cleaned, ["hello"])
        cleaned = cleaner.clean("hello world")
        eq_(cleaned, ["hello", "world"])

    def it_should_clean_text_test(self):
        cleaner = self.create_cleaner_with_stopwords()
        cleaned = cleaner.clean("Hello.")
        eq_(cleaned, ["hello"])
        cleaned = cleaner.clean("Hello, World!")
        eq_(cleaned, ["hello", "world"])
        cleaned = cleaner.clean("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec vulputate magna metus, sit amet pharetra eros volutpat vel. Fusce id. ")
        eq_(cleaned, ["lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipisc", "elit", "donec", "vulput", "magna", "metu", "sit", "amet", "pharetra", "ero", "volutpat", "vel", "fusc", "id"])

