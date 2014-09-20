__author__ = 'dzlab'

from unittest import TestCase
from nose.tools import *
from core.analyzer.language import LanguageAnalyzer
from core.helper import Comment


class UserTest(TestCase):

    def test_identifying_languages(self):
        analyzer = LanguageAnalyzer()
        comment = Comment()
        comment.message = "hello, the world is mine"
        analyzer.analyze(comment)
        eq_(len(analyzer.languages), 1)
        eq_('en' in analyzer.languages, True)
