# -*- coding: utf-8 -*-
__author__ = 'dzlab'

from unittest import TestCase
from core.model import Comment
from core.inout.reader import Reader
from nose.tools import *


class ReaderTest(TestCase):
    class FakeInput:

        def __init__(self):
            self.index = 0
            self.lines = ["\n"]
            self.lines.append("id:	10152075477696749_22524016")
            self.lines.append("from:	[Scott Duncan,	id:	1067564503]")
            self.lines.append("message:	'My monthly premium has increased over $100 monthly, while actual benefits have been stripped.  The deductible and out of pocket is so astronomical, that I would be financially ruined by the time the insurance provides any benefit.'")
            self.lines.append("created_time:	2014-01-16T21:11:26+0000")
            self.lines.append("like_count:	3")
            self.lines.append("\n")
            self.lines.append("id:	10152075477696749_22524023")
            self.lines.append("from:	[Debi Guenterberg,	id:	1446183585]")
            self.lines.append("message:	'Kevin. .and all Google Robert Guenterberg. The federal government helps the illegals!'")
            self.lines.append("created_time:	2014-01-16T21:11:46+0000")
            self.lines.append("like_count:	0")
            self.lines.append("\n")
            self.lines.append("id:	10152075477696749_22524033")
            self.lines.append("from:	[ياسرالنفيلي النفيلي,	id:	100004588261502]")
            self.lines.append("message:	u'\u0627\u0646\u0627 \u0644\u0628\u0627\u0621 \u0627\u0644\u0645\u0648\u0638\u0648\u0627\u0639 \u0627\u062a\u0631\u0627\u0643 \u0627\u0644\u0634\u062e\u0635 \u0627\u0644\u0630\u064a \u0639\u0631\u0627\u0642\u0644\u0648\u0627\u0646 \u0639\u0645\u0644\u064a\u062a \u0627\u0633\u0644\u0627\u0645 \u0648\u064a\u0639\u062a\u0645\u062f\u0627\u0648\u0639\u0644\u0627 \u0627\u0644\u0645\u0634\u0643\u0644 \u0648\u0627\u0644\u0641\u0648\u0627\u0636 \u0647\u0630\u0627 \u062a\u0641\u0643\u064a\u0631 \u062c\u0647\u0644\u0627 \u0648\u0644\u064a\u0627\u0633 \u062d\u0638\u0627\u0631\u0627'")
            self.lines.append("created_time:	2014-01-16T21:12:12+0000")
            self.lines.append("like_count:	0")

        def readline(self):
            if self.index == len(self.lines):
                return None
            line = self.lines[self.index]
            self.index += 1
            return line

    @staticmethod
    def create_reader():
        return Reader(comments_file=ReaderTest.FakeInput())

    def test_it_should_create_comment_from_lines(self):
        reader = ReaderTest.create_reader()
        comment = reader.next()
        eq_(comment.id, "10152075477696749_22524016")
        eq_(comment.user_name, "Scott Duncan")
        eq_(comment.user_id, "1067564503")
        eq_(comment.message, u'My monthly premium has increased over $100 monthly, while actual benefits have been stripped.  The deductible and out of pocket is so astronomical, that I would be financially ruined by the time the insurance provides any benefit.')
        eq_(comment.like_count, 3)
        comment = reader.next()
        comment = reader.next()
        eq_(comment.id, "10152075477696749_22524033")
        eq_(comment.user_name, "ياسرالنفيلي النفيلي")
        eq_(comment.user_id, "100004588261502")
        eq_(comment.message, u'\u0627\u0646\u0627 \u0644\u0628\u0627\u0621 \u0627\u0644\u0645\u0648\u0638\u0648\u0627\u0639 \u0627\u062a\u0631\u0627\u0643 \u0627\u0644\u0634\u062e\u0635 \u0627\u0644\u0630\u064a \u0639\u0631\u0627\u0642\u0644\u0648\u0627\u0646 \u0639\u0645\u0644\u064a\u062a \u0627\u0633\u0644\u0627\u0645 \u0648\u064a\u0639\u062a\u0645\u062f\u0627\u0648\u0639\u0644\u0627 \u0627\u0644\u0645\u0634\u0643\u0644 \u0648\u0627\u0644\u0641\u0648\u0627\u0636 \u0647\u0630\u0627 \u062a\u0641\u0643\u064a\u0631 \u062c\u0647\u0644\u0627 \u0648\u0644\u064a\u0627\u0633 \u062d\u0638\u0627\u0631\u0627')
        eq_(comment.like_count, 0)

    def test_it_should_consume_fake_input_file(self):
        comment = Comment()
        comments_file = ReaderTest.FakeInput()
        Reader.consume(comment, comments_file.readline())
        Reader.consume(comment, comments_file.readline())
        Reader.consume(comment, comments_file.readline())
        Reader.consume(comment, comments_file.readline())
        Reader.consume(comment, comments_file.readline())
        Reader.consume(comment, comments_file.readline())
        # check the parsed comment's information
        eq_(comment.id, "10152075477696749_22524016")
        eq_(comment.user_id, "1067564503")
        eq_(comment.user_name, "Scott Duncan")
        eq_(comment.message, u'My monthly premium has increased over $100 monthly, while actual benefits have been stripped.  The deductible and out of pocket is so astronomical, that I would be financially ruined by the time the insurance provides any benefit.')
        eq_(comment.like_count, 3)

    def test_it_should_consume_comment(self):
        comment = Comment()
        line = "id:	10152075477696749_22523804"
        Reader.consume(comment, line)
        line = "from:	[I fucking LOVE Chicago,	id:	691492767528100]"
        Reader.consume(comment, line)
        line = "message:	'Good job Mr. President!'"
        Reader.consume(comment, line)
        line = "created_time:	2014-01-16T21:04:23+0000"
        Reader.consume(comment, line)
        line = "like_count:	3"
        Reader.consume(comment, line)
        # check the parsed comment's information
        eq_(comment.id, "10152075477696749_22523804")
        eq_(comment.user_id, "691492767528100")
        eq_(comment.user_name, "I fucking LOVE Chicago")
        eq_(comment.message, u"Good job Mr. President!")
        eq_(comment.like_count, 3)

    def test_special_lines_from(self):
        """Test the result of parsing some lines starting with 'from'"""
        comment = Comment()
        line = "from:	[I’m Not Saying It Was Aliens But, It Was Aliens,	id:	255914607784724]"
        Reader.consume(comment, line)
        eq_(comment.user_id, "255914607784724")
        eq_(comment.user_name, "I’m Not Saying It Was Aliens But, It Was Aliens")
        comment = Comment()
        line = "from:	[,	id:	]"
        Reader.consume(comment, line)
        eq_(comment.user_id, None)
        eq_(comment.user_name, None)
