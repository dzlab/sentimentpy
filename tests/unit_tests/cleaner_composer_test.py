__author__ = 'dzlab'

from unittest import TestCase
from sentimentpy.cleaner import CleanerComposer
from nose.tools import *


class CleanerComposerTest(TestCase):

    def test_composing_methods(self):
        cleaner = CleanerComposer()
        eq_(cleaner.clean('hello word'), 'hello word', "The identity method should be called when no composition")
        cleaner.normalize()
        eq_(cleaner.clean('HELLO WorD'), 'hello word', "The normalize method should be called to lower text")
        cleaner.normalize()
        eq_(cleaner.clean('HELLO WorD'), 'hello word', "Composing two normalize() should have no effect more than lower")
        cleaner.normalize()