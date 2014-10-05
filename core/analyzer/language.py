__author__ = 'dzlab'

import logging

from core.analyzer import Analyzer
from core.inout.writer import BufferedWriter
from core.helper import WatchTime, guess_language_thread_safe


class LanguageAnalyzer(Analyzer):
    logger = logging.getLogger('LanguageAnalyzer')

    def __init__(self):
        self.languages = {}
        self.watch = WatchTime()

    def analyze(self, comment):
        self.watch.start()
        language = guess_language_thread_safe(comment.message.strip("'"))
        if language == 'UNKNOWN':
            self.logger.debug("Failed to guess the language for: %s", comment.message)
        comment.set_language(language)
        if not language in self.languages:
            self.languages[language] = 0
        self.languages[language] += 1
        self.watch.stop()
        #self.logger.debug("Comment's language guessed as %s in %s seconds", language, str(end_time - start_time))

    def finalize(self, output=None, close=True):
        self.logger.info('Analyzing the comments took %s seconds' % str(self.watch.total()))
        self.watch.reset()
        # start a new watch
        self.watch.start()
        if not output:
            output = BufferedWriter(filename='piechart.json', file_format='json')
        output.header('var labels = [')
        for language in self.languages:
            data = "{ \"label\": \"%s\", \"value\": %s }" % (language, str(self.languages[language]))
            output.append(data)
        output.footer(']')
        if close:
            output.close()
        self.watch.stop()
        self.logger.info('Finalization took %s seconds' % str(self.watch.total()))

