__author__ = 'dzlab'

from sentimentpy.helper import Comment, WatchTime
from dateutil import parser
from ast import literal_eval
import logging


class Reader:
    """a reader helper for reading comments from a file"""
    logger = logging.getLogger('Reader')

    #comments_file = None

    def __init__(self, comments_file=None, filename=None):
        if comments_file:
            self.comments_file = comments_file
        elif filename:
            self.comments_file = open(filename, 'r')
        self.watch = WatchTime()

    def close(self):
        self.comments_file.close()

    def next(self):
        """gives the next comment"""
        self.watch.start()
        line = self.comments_file.readline()
        if not line:
            self.watch.stop()
            self.logger.debug('Finished reading from input file in %s seconds' % str(self.watch.total()))
            return None
        comment = Comment()
        self.consume_(comment, self.comments_file.readline())
        self.consume_(comment, self.comments_file.readline())
        self.consume_(comment, self.comments_file.readline())
        self.consume_(comment, self.comments_file.readline())
        self.consume_(comment, self.comments_file.readline())
        self.watch.stop()
        return comment

    @staticmethod
    def consume_(comment, line):
        """consumes a line to update the corresponding comment information
        :param comment -- the comment object to update its information
        :param line -- the line to be parsed
        :rtype : True if the parsed line for this comment is valid
        """
        if line.startswith("id:	"):
            comment.id = line[len("id:	"):len(line)]
        elif line.startswith("from:	"):
            blocks = line[len("from:	"):len(line)].strip().replace('[', '').replace(']', '').split(',')
            comment.user_name = blocks[0]
            comment.user_id = blocks[1].strip('\t').split('\t')[1]
        elif line.startswith("message:	"):
            message = line[len("message:	"):len(line)].strip()
            if not message.startswith("u'"):
                comment.message = unicode(message.strip("'"))
            else:
                comment.message = literal_eval(message)
        elif line.startswith("created_time:	"):
            string_time = line[len("created_time:	"):len(line)]
            comment.created_time = parser.parse(string_time)
        elif line.startswith("like_count:	"):
            comment.like_count = int(line[len("like_count:	"):len(line)])
        else:
            Reader.logger.warn("Unrecognized information in: %s", line)

