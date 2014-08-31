__author__ = 'dzlab'

from unittest import TestCase
from nose.tools import *
from sentimentpy.analyzer.language import LanguageAnalyzer
from sentimentpy.helper import Comment


class UserTest(TestCase):

    def test_identifying_languages(self):
        analyzer = LanguageAnalyzer()
        comment = Comment()
        comment.message = "hello world"
        analyzer.analyze(comment)
        eq_(len(analyzer.languages), 1)
        eq_(u'en' in analyzer.languages, True)
