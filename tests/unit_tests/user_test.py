__author__ = 'dzlab'

from unittest import TestCase
from nose.tools import *
from sentimentpy.analyzer.user import UserAnalyzer
from sentimentpy.helper import Comment
from cleaner_test import CleanerTest


class UserTest(TestCase):

    def it_should_map_text_by_user_test(self):
        analyzer = UserAnalyzer(CleanerTest.create_cleaner_with_stopwords(''))
        comment = Comment()
        comment.user_id = "0123456789"
        comment.user_name = "user1"
        comment.message = "hello"
        analyzer.analyze(comment)
        eq_(analyzer.names_by_id["0123456789"], "user1")
        eq_(analyzer.texts_by_id["0123456789"], "hello")
        #trying with a second message from same user
        comment.message = "world!"
        analyzer.analyze(comment)
        eq_(analyzer.texts_by_id["0123456789"], "hello world")
        eq_(len(analyzer.names_by_id), 1)
        eq_(len(analyzer.texts_by_id), 1)
        #trying with a longer message
        comment.user_id = "0000000000"
        comment.user_name = "user2"
        comment.message = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec vulputate magna metus, sit amet pharetra eros volutpat vel. Fusce id. "
        analyzer.analyze(comment)
        eq_(analyzer.texts_by_id["0000000000"], "lorem ipsum dolor sit amet consectetur adipisc elit donec vulput magna metu sit amet pharetra ero volutpat vel fusc id")
        eq_(len(analyzer.names_by_id), 2)
        eq_(len(analyzer.texts_by_id), 2)