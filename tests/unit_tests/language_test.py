__author__ = 'dzlab'

from unittest import TestCase
from nose.tools import *
from core.analyzer.language import LanguageAnalyzer
from core.model import Comment
from core.inout.writer import Formatter


class FakeWriter:
    def __init__(self):
        self.closed = False
        self.formatter = Formatter
        self.h = ''
        self.content = ''
        self.f = ''

    def header(self, header):
        self.h = header

    def footer(self, footer):
        self.f = footer

    def append(self, data):
        self.content += str(data)

    def close(self):
        self.closed = True


class LanguageTest(TestCase):

    def test_identifying_languages(self):
        analyzer = LanguageAnalyzer()
        comment = Comment()
        comment.message = "hello, the world is mine"
        analyzer.analyze(comment)
        eq_(len(analyzer.languages), 1)
        eq_('en' in analyzer.languages, True)

    def test_finalize_output(self):
        analyzer = LanguageAnalyzer()
        comment = Comment()
        comment.message = 'I have a dream that one day this nation will rise up and live out the true meaning of its creed:"We hold these truths to be self-evident: that all men are created equal"'
        analyzer.analyze(comment)
        output = FakeWriter()
        analyzer.finalize(output, True)
        eq_('var labels = [', output.h, "The output header should be set")
        eq_("{'value': 1, 'label': u'en'}", output.content, "The output content should be set")
        eq_(']', output.f, "The output footer should be set")
        eq_(True, output.closed, "The output should be closed")
