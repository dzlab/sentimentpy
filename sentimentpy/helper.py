import os
from dateutil import parser
import logging

# a class representation of a comment
class Comment:
   message = None
   created_time = None

   #def __init__(self):
      
# a reader helper for reading comments from a file
class Reader:
   logger = logging.getLogger('Reader')
   FILENAME = '6815841748_10152075477696749.txt'
   COMMENTS_FILE = '%s/../data/%s' % (os.path.dirname(os.path.realpath(__file__)), FILENAME)

   comments_file = None

   def __init__(self):   
      self.comments_file = open(Reader.COMMENTS_FILE, 'r')

   def close(self):
      self.comments_file.close()

   def next(self):
      line = self.comments_file.readline()
      if not line:
         self.logger.debug('No information found on current line %s', line)
         return None
      comment = Comment()
      self._consume(comment, self.comments_file.readline())
      self._consume(comment, self.comments_file.readline())
      self._consume(comment, self.comments_file.readline())
      self._consume(comment, self.comments_file.readline())
      self._consume(comment, self.comments_file.readline())
      self.logger.debug('Parsed %s', comment)
      return comment

   def _consume(self, comment, line):
      if line.startswith("message:	"):
         self.logger.debug('Consuming message from line \n %s', line)
         comment.message = line[len("message:	")+1:len(line)-2]
      elif line.startswith("created_time:	"):
         self.logger.debug('Consuming creation date from line \n %s', line)
         string_time = line[len("created_time:	"):len(line)]
         comment.created_time = parser.parse(string_time)

# a writer helper
class Writer:
   COMMENTS_FILE = '%s/../output/data.tsv' % os.path.dirname(os.path.realpath(__file__))
   output = None

   def __init__(self, filename=None):
      if not filename:
         filename = Writer.COMMENTS_FILE
      self.output = open(filename, 'w')

   def header(self, line):
      self.append(line)

   def append(self, line):
      self.output.write(line + '\n')
   
   def close(self):
      self.output.close()


