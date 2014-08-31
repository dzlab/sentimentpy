__author__ = 'dzlab'

from unittest import TestCase
from nose.tools import *
from sentimentpy.analyzer.user import UserAnalyzer
from sentimentpy.helper import Comment
from cleaner_test import CleanerTest


class UserTest(TestCase):

    def test_mapping_text_by_user(self):
        analyzer = UserAnalyzer(CleanerTest.create_cleaner_with_stopwords(''))
        comment = Comment()
        comment.user_id = "0123456789"
        comment.user_name = "user1"
        comment.message = "hello"
        analyzer.analyze(comment)
        eq_(analyzer.names_by_id["0123456789"], "user1")
        eq_(analyzer.texts_by_id["0123456789"], {u'UNKNOWN': 'hello'})
        #trying with a second message from same user
        comment.message = "world!"
        analyzer.analyze(comment)
        eq_(analyzer.texts_by_id["0123456789"], {u'UNKNOWN': 'hello world'})
        eq_(len(analyzer.names_by_id), 1)
        eq_(len(analyzer.texts_by_id), 1)
        #trying with a longer message
        comment.user_id = "0000000000"
        comment.user_name = "user2"
        comment.message = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec vulputate magna metus, sit amet pharetra eros volutpat vel. Fusce id. "
        analyzer.analyze(comment)
        eq_(analyzer.texts_by_id["0000000000"], {u'la': "lorem ipsum dolor sit amet consectetur adipisc elit donec vulput magna metu sit amet pharetra ero volutpat vel fusc id"})
        eq_(len(analyzer.names_by_id), 2)
        eq_(len(analyzer.texts_by_id), 2)

    def test_updating_distance_matrix(self):
        analyzer = UserAnalyzer(CleanerTest.create_cleaner_with_stopwords(''))
        eq_(analyzer.dist_matrix, {}, "Initially the distance matrix should be empty")

        analyzer.update_distance_matrix(None, None, None, 0)
        eq_(analyzer.dist_matrix, {}, "Non valid indexes should not affect the distance matrix")

        analyzer.update_distance_matrix(None, "000", 'en', 0.5)
        eq_(analyzer.dist_matrix, {}, "Non valid indexes should not affect the distance matrix")

        analyzer.update_distance_matrix("0", "1", 'en', 0.5)
        eq_(analyzer.dist_matrix, {'0': {'en': {'1': 0.5}}, '1': {'en': {'0': 0.5}}}, "Cells should be updated with the distance")

    def test_generating_frequency_vector(self):
        analyzer = UserAnalyzer(CleanerTest.create_cleaner_with_stopwords(''))
        eq_(analyzer.generate_frequency_vector(None, None), None, "Should not handle non valid input")
        analyzer.texts_by_id['0'] = {}
        analyzer.texts_by_id['0']['en'] = "hello world"
        eq_(analyzer.generate_frequency_vector('0', 'en'), {'world': 0.5, 'hello': 0.5}, "Both words should have half frequency")

    def test_generating_distance_matrix(self):
        analyzer = UserAnalyzer(CleanerTest.create_cleaner_with_stopwords(''))
        analyzer.generate_distance_matrix()
        eq_(analyzer.dist_matrix, {}, "Distance matrix should be empty as there is no text")

        analyzer.texts_by_id['0'] = {}
        analyzer.texts_by_id['0']['en'] = "hello world"
        analyzer.generate_distance_matrix()
        eq_(analyzer.dist_matrix, {}, "Distance matrix should be empty as there is only one text for a user/language pair")

        analyzer.texts_by_id['1'] = {}
        analyzer.generate_distance_matrix()
        eq_(analyzer.dist_matrix, {}, "Distance matrix should be empty as there is no language match for the two users")

        analyzer.texts_by_id['2'] = {}
        analyzer.texts_by_id['2']['en'] = "hello, the world is mine"
        analyzer.generate_distance_matrix()
        expected = {'0': {'en': {'2': 0.5477225575051662}}, '2': {'en': {'0': 0.5477225575051662}}}
        eq_(analyzer.dist_matrix, expected, "Distance matrix should be empty as there is no language match for the two users")