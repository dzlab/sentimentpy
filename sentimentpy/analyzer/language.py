__author__ = 'dzlab'

from analyzer import *
from sentimentpy.helper import BufferedWriter
from guess_language import guessLanguage
from time import time
import logging


class LanguageAnalyzer(Analyzer):
    logger = logging.getLogger('LanguageAnalyzer')
    languages = {}

    def __init__(self):
        return

    def analyze(self, comment):
        start_time = time()
        language = guessLanguage(comment.message)
        if language == 'UNKNOWN':
            self.logger.debug("Failed to guess the language for: %s", comment.message)
        if not language in self.languages:
            self.languages[language] = 0
        self.languages[language] += 1
        end_time = time()
        #self.logger.debug("Comment's language guessed as %s in %s seconds", language, str(end_time - start_time))

    def finalize(self):
        start_time = time()
        writer = BufferedWriter('piechart.json')
        writer.header('var labels = [')
        first = True
        for language in self.languages:
            if first:
                line = "  "
                first = False
            else:
                line = "  ,"
            line += "{ \"label\": \"%s\", \"value\": %s }" % (language, str(self.languages[language]))
            writer.append(line)
        writer.footer(']')
        writer.close()
        end_time = time()
        self.logger.info('Finalization took %s seconds' % str(end_time - start_time))

