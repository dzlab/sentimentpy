__author__ = 'dzlab'

from core.analyze import *
from core.model import Comment
from nose.tools import *
from unittest import TestCase


class AnalyzerTest(TestCase):

    class FakeAnalyzer:
        def __init__(self):
            self.analyze_calls_count = 0
            self.finalize_calls_count = 0

        def analyze(self, comment):
            self.analyze_calls_count += 1

        def finalize(self):
            self.finalize_calls_count += 1

    def test_analyzer_call_times_by_worker(self):
        comments = Queue(1)
        analyzer = AnalyzerTest.FakeAnalyzer()
        worker = AnalyzerWorker(analyzer, comments)
        count = 10
        for i in range(count):
            comments.put(Comment())
        comments.join()
        eq_(analyzer.analyze_calls_count, count, "The number of calls to the analyzer should be %d" % count)

    def test_analyzer_call_times_by_manager(self):
        manager = AnalyzerManager(3)
        analyzer1 = AnalyzerTest.FakeAnalyzer()
        analyzer2 = AnalyzerTest.FakeAnalyzer()
        manager.register(analyzer1)
        manager.register(analyzer2)
        count = 10
        for i in range(count):
            manager.process(Comment())
        manager.finalize()
        # check the number of calls to analyze()
        eq_(analyzer1.analyze_calls_count, count, "The number of calls to the analyzer should be %d" % count)
        eq_(analyzer2.analyze_calls_count, count, "The number of calls to the analyzer should be %d" % count)
        # check the number of calls to finalize()
        eq_(analyzer1.analyze_calls_count, count, "The number of calls to the analyzer should be %d" % count)
        eq_(analyzer2.analyze_calls_count, count, "The number of calls to the analyzer should be %d" % count)