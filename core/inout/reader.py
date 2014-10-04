__author__ = 'dzlab'

from core.model import Comment
from core.helper import WatchTime
from dateutil import parser
from ast import literal_eval
import logging
import traceback


class Reader:
    """a reader helper for reading comments from a file"""
    logger = logging.getLogger('Reader')

    #comments_file = None

    def __init__(self, comments_file=None, filename=None, parse=True):
        if comments_file:
            self.comments_file = comments_file
        elif filename:
            self.comments_file = open(filename, 'r')
        self.watch = WatchTime()
        self.parse = parse

    def close(self):
        self.comments_file.close()

    def next(self):
        """gives the next comment"""
        self.watch.start()
        line = self.comments_file.readline()
        if not line:
            self.watch.stop()
            self.logger.debug('Finished reading from %s in %f seconds' % (self.comments_file.name, self.watch.total()))
            return None
        comment = Comment()
        self.safely_consume(comment, self.comments_file.readline())
        self.safely_consume(comment, self.comments_file.readline())
        self.safely_consume(comment, self.comments_file.readline())
        self.safely_consume(comment, self.comments_file.readline())
        self.safely_consume(comment, self.comments_file.readline())
        self.watch.stop()
        return comment

    def safely_consume(self, comment, line):
        try:
            self.consume(comment, line)
        except Exception, err:
            Reader.logger.info("Failed to parse: %s caused by %s" % (line, err.message))
            print traceback.print_exc()

    def consume(self, comment, line):
        """consumes a line to update the corresponding comment information
        :param comment -- the comment object to update its information
        :param line -- the line to be parsed
        :rtype : True if the parsed line for this comment is valid
        """
        if line.startswith("id:	"):
            comment.id = line[len("id:	"):len(line)]
        elif line.startswith("from:	"):
            blocks = line[len("from:	"):len(line)].strip().replace('[', '').replace(']', '').rsplit(',', 1)
            if blocks[0] and blocks[0] != '':
                comment.user_name = blocks[0]
            else:
                Reader.logger.info("Empty user_name in: %s" % line)
            blocks = blocks[1].strip('\t').split('\t')
            if len(blocks) == 2:
                comment.user_id = blocks[1]
            else:
                Reader.logger.info("Could not find user_id in: %s" % line)
        elif line.startswith("message:	"):
            message = line[len("message:	"):len(line)].strip()
            if not message.startswith("u'"):
                comment.message = unicode(message.strip("'"))
            else:
                comment.message = literal_eval(message)
        elif line.startswith("created_time:	"):
            string_time = line[len("created_time:	"):len(line)]
            if self.parse:
                comment.created_time = parser.parse(string_time)
            else:
                comment.created_time = string_time
        elif line.startswith("like_count:	"):
            comment.like_count = int(line[len("like_count:	"):len(line)])
        else:
            Reader.logger.warn("Unrecognized information in: %s", line)

