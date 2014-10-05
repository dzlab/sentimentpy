__author__ = 'dzlab'

import os
import logging
from core.helper import WatchTime


COMMENTS_FILE = '%s/../../output/' % os.path.dirname(os.path.realpath(__file__))


class Formatter:
    def __init__(self, file_format='csv'):
        self.first = True
        self.file_format = file_format

    def format(self, data):
        if data is '':
            return data
        formatted = data
        if self.file_format == 'csv':
            formatted += '\n'
        elif self.file_format == 'json':
            if self.first:
                self.first = False
            else:
                formatted = ',' + formatted
        return formatted


class Writer:
    """a writer helper"""
    #output = None
    logger = logging.getLogger('Writer')

    def __init__(self, filename=None, file_format='csv'):
        if not filename:
            filename = 'data.tsv'
        self.formatter = Formatter(file_format)
        self.output = open(COMMENTS_FILE+filename, 'wb')
        self.watch = WatchTime()

    def header(self, header):
        line = header + '\n'
        self.output.write(line)

    def append(self, data):
        if not data or data is '':
            return
        self.watch.start()
        line = self.formatter.format(str(data))
        self.output.write(line)
        self.watch.stop()

    def footer(self, line):
        self.output.write(line)

    def close(self):
        self.watch.start()
        self.output.close()
        self.watch.stop()
        Writer.logger.debug('Finished writing to output file in %s seconds' % str(self.watch.total()))


class BufferedWriter(Writer):
    """a writer helper that uses a buffer to accumulate lines before writer to disk"""
    #buffer = ''
    filename = 'data.tsv'

    def __init__(self, output=None, filename=None, block=100, file_format='csv'):
        if output:
            self.output = output
        else:
            if filename:
                self.filename = filename
            self.output = open(COMMENTS_FILE + self.filename, 'wb')
        self.formatter = Formatter(file_format)
        self.block = block
        self.buffer = ''
        self.counter = 0
        self.watch = WatchTime()

    def append_to_buffer(self, line):
        """Add a line to buffer, write to disk if buffer full"""
        self.buffer += line
        self.counter += 1
        if self.counter == self.block:
            self.output.write(self.buffer)
            self.counter = 0
            self.buffer = ''

    def header(self, line):
        self.append_to_buffer(line)

    def append(self, data):
        if not data or data is '':
            return
        self.watch.start()
        self.append_to_buffer(self.formatter.format(str(data)))
        self.watch.stop()

    def footer(self, line):
        self.append_to_buffer(line)

    def close(self):
        self.watch.start()
        self.output.write(self.buffer)
        self.output.close()
        self.watch.stop()
        Writer.logger.debug('Finished writing to output file in %s seconds' % str(self.watch.total()))


class MongodbWriter:
    """a writer helper that wraps a mongodb connection"""
    #output = None
    logger = logging.getLogger('MongodbWriter')

    def __init__(self, mongodb, collection):
        if not mongodb:
            raise Exception("Need mongodb connection client")
        self.output = mongodb.sentimentdb
        self.collection = collection
        if collection not in self.output.collection_names():
            self.logger.debug("Cannot find collection '%s' not in database" % collection)
            #output.[collection]. = []
        self.watch = WatchTime()

    def header(self, line):
        self.logger.info("Ignoring header %s" % line)
        pass

    def append(self, document):
        self.watch.start()
        self.output[self.collection].insert(document)
        self.watch.stop()

    def footer(self, line):
        self.logger.info("Ignoring footer %s" % line)
        pass

    def close(self):
        Writer.logger.debug('Finished writing to output mongodb in %s seconds' % str(self.watch.total()))
