__author__ = 'dzlab'

import os
import logging
from sentimentpy.helper import WatchTime


COMMENTS_FILE = '%s/../../output/' % os.path.dirname(os.path.realpath(__file__))


class Writer:
    """a writer helper"""
    #output = None
    logger = logging.getLogger('Writer')

    def __init__(self, filename=None):
        if not filename:
            filename = 'data.tsv'
        self.output = open(COMMENTS_FILE+filename, 'wb')
        self.watch = WatchTime()

    def header(self, line):
        self.append(line)

    def append(self, line):
        self.watch.start()
        self.output.write(line + '\n')
        self.watch.stop()

    def footer(self, line):
        self.append(line)

    def close(self):
        self.watch.start()
        self.output.close()
        self.watch.stop()
        Writer.logger.debug('Finished writing to output file in %s seconds' % str(self.watch.total()))



class BufferedWriter(Writer):
    """a writer helper that uses a buffer to accumulate lines before writer to disk"""
    #buffer = ''
    filename = 'data.tsv'

    def __init__(self, output=None, filename=None, block=100):
        if output:
            self.output = output
        else:
            if filename:
                self.filename = filename
            self.output = open(COMMENTS_FILE + self.filename, 'wb')
        self.block = block
        self.buffer = ''
        self.counter = 0
        self.watch = WatchTime()

    def header(self, line):
        self.append(line)

    def append(self, line):
        if line is '':
            return
        self.watch.start()
        self.buffer += line + '\n'
        self.counter += 1
        if self.counter == self.block:
            self.output.write(self.buffer)
            self.counter = 0
            self.buffer = ''
        self.watch.stop()

    def footer(self, line):
        self.append(line)

    def close(self):
        self.watch.start()
        self.output.write(self.buffer)
        self.output.close()
        self.watch.stop()
        Writer.logger.debug('Finished writing to output file in %s seconds' % str(self.watch.total()))