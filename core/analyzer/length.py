from time import time
import logging

import numpy
from core.analyzer import Analyzer
from core.inout.writer import BufferedWriter


class LengthAnalyzer(Analyzer):
    """Generate a heat map for comments length
    """
    logger = logging.getLogger('LengthAnalyzer')

    len_mat = None
    freq_mat = None
    avg_len_mat = None

    def __init__(self):
        # initiating matrix variables
        self.len_mat = numpy.zeros(7 * 24, dtype=int).reshape(7, 24)
        self.freq_mat = numpy.zeros((7, 24), int)
        self.avg_len_mat = numpy.zeros((7, 24), int)

    def name(self):
        return 'length'

    def analyze(self, comment):
        if not comment:
            return
        # calculating comment's lengths
        day = comment.created_time.weekday()
        hour = comment.created_time.hour
        value = len(comment.message.strip("'"))
        self.len_mat[day][hour] += value
        self.freq_mat[day][hour] += 1

    def finalize(self, output=None, close=True):
        # calculate average length for each (day, hour) peer
        start_time = time()
        for d in range(7):
            for h in range(24):
                if self.freq_mat[d][h] == 0:
                    avg_val = 0
                else:
                    avg_val = self.len_mat[d][h] / self.freq_mat[d][h]
                self.avg_len_mat[d][h] = round(avg_val)

        # writing the result to data.tsv
        if not output:
            output = BufferedWriter()
        output.header('day' + '\t' + 'hour' + '\t' + 'value')
        for d in range(7):
            for h in range(24):
                data = str(d+1) + '\t' + str(h+1) + '\t' + str(self.avg_len_mat[d][h])
                output.append(data)
      
        if close:
            output.close()
        end_time = time()
        self.logger.info('Finalization took %s seconds' % str(end_time - start_time))
