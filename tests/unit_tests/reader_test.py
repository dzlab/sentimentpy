__author__ = 'dzlab'

from unittest import TestCase
from sentimentpy.helper import Comment
from sentimentpy.io.reader import Reader
from nose.tools import *


class ReaderTest(TestCase):

    def it_should_consume_comment_test(self):
        comment = Comment()
        line = "id:	10152075477696749_22523804"
        Reader._consume(comment, line)
        line = "from:	[I fucking LOVE Chicago,	id:	691492767528100]"
        Reader._consume(comment, line)
        line = "message:	'Good job Mr. President!'"
        Reader._consume(comment, line)
        line = "created_time:	2014-01-16T21:04:23+0000"
        Reader._consume(comment, line)
        line = "like_count:	3"
        Reader._consume(comment, line)
        # check the parsed comment's information
        eq_(comment.id, "10152075477696749_22523804")
        eq_(comment.user_id, "691492767528100")
        eq_(comment.user_name, "I fucking LOVE Chicago")
        eq_(comment.message, u"Good job Mr. President!")
        eq_(comment.like_count, 3)
