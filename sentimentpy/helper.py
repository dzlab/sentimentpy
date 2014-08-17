import os
from dateutil import parser
import logging


class Comment:
    """a class representation of a comment"""
    message = None
    created_time = None

    def __init__(self):
        return
      

class Reader:
    """a reader helper for reading comments from a file"""
    logger = logging.getLogger('Reader')
   
    comments_file = None

    def __init__(self, filename):
        self.comments_file = open(filename, 'r')

    def close(self):
        self.comments_file.close()

    def next(self):
        line = self.comments_file.readline()
        if not line:
            self.logger.debug('Finished reading from input file')
            return None
        comment = Comment()
        self._consume(comment, self.comments_file.readline())
        self._consume(comment, self.comments_file.readline())
        self._consume(comment, self.comments_file.readline())
        self._consume(comment, self.comments_file.readline())
        self._consume(comment, self.comments_file.readline())
        return comment

    def _consume(self, comment, line):
        if line.startswith("message:	"):
            comment.message = line[len("message:	")+1:len(line)-2]
        elif line.startswith("created_time:	"):
            string_time = line[len("created_time:	"):len(line)]
            comment.created_time = parser.parse(string_time)


class Writer:
    """a writer helper"""
    COMMENTS_FILE = '%s/../output/' % os.path.dirname(os.path.realpath(__file__))
    output = None

    def __init__(self, filename=None):
        if not filename:
            filename = 'data.tsv'
        self.output = open(Writer.COMMENTS_FILE+filename, 'wb')

    def header(self, line):
        self.append(line)

    def append(self, line):
        self.output.write(line + '\n')

    def footer(self, line):
        self.append(line)

    def close(self):
        self.output.close()


class BufferedWriter(Writer):
    """a writer helper that uses a buffer to accumulate lines before writer to disk"""
    COMMENTS_FILE = '%s/../output/' % os.path.dirname(os.path.realpath(__file__))
    buffer = ''
    filename = 'data.tsv'

    def __init__(self, filename=None):
        if filename:
            self.filename = filename

    def header(self, line):
        self.append(line)

    def append(self, line):
        self.buffer += line + '\n'

    def footer(self, line):
        self.append(line)

    def close(self):
        self.output = open(Writer.COMMENTS_FILE + self.filename, 'wb')
        self.output.write(self.buffer)
        self.output.close()
