__author__ = 'dzlab'

from analyzer import *
from sentimentpy.io.writer import BufferedWriter
from sentimentpy.helper import WatchTime
from guess_language import guess_language
from time import time
import logging


class LanguageAnalyzer(Analyzer):
    logger = logging.getLogger('LanguageAnalyzer')

    def __init__(self):
        self.languages = {}
        self.watch = WatchTime()

    def analyze(self, comment):
        self.watch.start()
        language = guess_language(comment.message.strip("'"))
        if language == 'UNKNOWN':
            self.logger.debug("Failed to guess the language for: %s", comment.message)
        comment.language = language
        if not language in self.languages:
            self.languages[language] = 0
        self.languages[language] += 1
        self.watch.stop()
        #self.logger.debug("Comment's language guessed as %s in %s seconds", language, str(end_time - start_time))

    def finalize(self):
        self.logger.info('Analyzing the comments took %s seconds' % str(self.watch.total()))
        self.watch.reset()
        # start a new watch
        self.watch.start()
        output = BufferedWriter(filename='piechart.json')
        output.header('var labels = [')
        first = True
        for language in self.languages:
            if first:
                line = "  "
                first = False
            else:
                line = "  ,"
            line += "{ \"label\": \"%s\", \"value\": %s }" % (language, str(self.languages[language]))
            output.append(line)
        output.footer(']')
        output.close()
        self.watch.stop()
        self.logger.info('Finalization took %s seconds' % str(self.watch.total()))

