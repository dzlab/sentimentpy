__author__ = 'dzlab'

from unittest import TestCase
from nose.tools import *
from core.analyzer.user import UserAnalyzer
from core.helper import Comment


class UserAnalysisTest(TestCase):

    def setUp(self):
        c1 = Comment()
        c1.message = "Hello world!"
        c1.id = "00001"
        c1.user_id = "01"
        c1.user_name = "u1"
        c2 = Comment()
        c2.message = "So, if on advanced addition, absolute I may received replying throwing he. Delighted, consisted the newspaper of unfeeling as we neglected. Do Tell size come hard mrs and four fond are?"
        c2.id = "00002"
        c2.user_id = "02"
        c2.user_name = "u2"
        self.comments = [c1, c2]

    def it_should_analyze_text_test(self):
        analyzer = UserAnalyzer()
        for comment in self.comments:
            analyzer.analyze(comment)
        # check how is cleaned the first message
        eq_(analyzer.names_by_id["01"], "u1")
        eq_(analyzer.texts_by_id["01"], {u'UNKNOWN': 'world'})
        # check how is cleaned the first message
        eq_(analyzer.names_by_id["02"], "u2")
        eq_(analyzer.texts_by_id["02"], {u'en': "advanc addit absolut mai receiv repli throw delight consist newspap unfeel neglect size hard mr fond ar"})