from helper import *
import logging
import numpy

class Analyzer:

   reader = None
   writer = None

   def __init__(self):
      return

   def generate_length_heatmap(self):      
      self.reader = Reader()
      # initiating matrix variables
      len_mat = numpy.zeros(7 * 24, dtype=int).reshape(7, 24)
      freq_mat= numpy.zeros((7, 24), int)      
      # calculating comment's lengths 
      while True:   
         comment = self.reader.next()
         if not comment: break
         day = comment.created_time.weekday()
         hour = comment.created_time.hour
         value = len(comment.message)
         len_mat[day][hour] = len_mat[day][hour] + value   
         freq_mat[day][hour] = freq_mat[day][hour] + 1

      self.reader.close()
      # calculate average length for each (day, hour) peer
      avg_len_mat= numpy.zeros((7, 24), int)
      for d in range(7):
         for h in range(24):       
            if freq_mat[d][h] == 0: 
               avg_val = 0
            else : 
               avg_val = len_mat[d][h] / freq_mat[d][h]
            avg_len_mat[d][h] = round(avg_val)

      # writting the result to data.tsv
      self.writer = Writer()
      self.writer.header('day' + '\t' + 'hour' + '\t' + 'value')
      for d in range(7):
         for h in range(24):       
            self.writer.append(str(d+1) + '\t' + str(h+1) + '\t'  + str(avg_len_mat[d][h]))
      
      self.writer.close()

if __name__ == '__main__':
   logging.basicConfig(level=logging.DEBUG)
   analyzer = Analyzer()
   analyzer.generate_length_heatmap()

