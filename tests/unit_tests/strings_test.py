__author__ = 'dzlab'

from unittest import TestCase
from nose.tools import *
from core.utils.strings import StringUtils


class StringUtilsTest(TestCase):

    def test_frequency_empty_text(self):
        word_freq = StringUtils.word_frequency("")
        eq_(word_freq, {})

    def test_word_frequency_one_occurrence(self):
        word_freq = StringUtils.word_frequency('lorem')
        eq_(word_freq, {'lorem': 1}, "A phrase of one word should have a frequency 1")
        word_freq = StringUtils.word_frequency('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas sapien. ')
        eq_(word_freq, {'Lorem': 0.1, 'ipsum': 0.1, 'dolor': 0.1, 'sit': 0.1, 'amet': 0.1, 'consectetur': 0.1, 'adipiscing': 0.1, 'elit': 0.1, 'Maecenas': 0.1, 'sapien': 0.1})

    def test_word_frequency_multi_occurrence(self):
        word_freq = StringUtils.word_frequency("it's not what you look at that matters, it's what you see")
        eq_(word_freq, {'it':0.14285714285714285, 's':0.14285714285714285, 'not':0.07142857142857142, 'what':0.14285714285714285, 'you':0.14285714285714285, 'look':0.07142857142857142, 'at':0.07142857142857142, 'that':0.07142857142857142, 'matters':0.07142857142857142, 'see':0.07142857142857142})

    def test_distance_empty_vectors(self):
        w1 = {}
        w2 = {}
        eq_(StringUtils.words_distance(w1, w2), 0)
        w1 = {'hello': 0.5, 'word': 0.5}
        w2 = {}
        eq_(StringUtils.words_distance(w1, w2), 0.7071067811865476)
        w1 = {}
        w2 = {'lorem': 0.2, 'ipsum': 0.2, 'dolor':0.2, 'sit':0.2, 'amet':0.2}
        eq_(StringUtils.words_distance(w1, w2), 0.447213595499958)