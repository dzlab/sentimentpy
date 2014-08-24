from __future__ import division
import os, sys
from datetime import datetime
import numpy

from helper import *

reader = Reader()

len_mat = numpy.zeros(7 * 24, dtype=int).reshape(7, 24)
freq_mat= numpy.zeros((7, 24), int)
avg_len_mat= numpy.zeros((7, 24), int)

while True:   
   comment = reader.next()
   if not comment: break
   day = comment.created_time.weekday()
   hour = comment.created_time.hour
   value = len(comment.message)   
   len_mat[day][hour] = len_mat[day][hour] + value   
   freq_mat[day][hour] = freq_mat[day][hour] + 1

reader.close()

output = open('%s/../html/data.tsv' % os.path.dirname(os.path.realpath(__file__)), 'w')
output.write('day' + '\t' + 'hour' + '\t' + 'value' + '\n')

avg_min = sys.maxint
avg_max = 0

for d in range(7):
   for h in range(24):       
       if freq_mat[d][h] == 0: 
          avg_val = 0
       else : 
          avg_val = len_mat[d][h] / freq_mat[d][h]
       if avg_val > avg_max:
          avg_max = avg_val
       if avg_val < avg_min:
          avg_min = avg_val       
       avg_len_mat[d][h] = avg_val

bucket_size = (avg_max - avg_min) / 10

for d in range(7):
   for h in range(24):
       bucket_number = round(avg_len_mat[d][h] / bucket_size)
       output.write(str(d) + '\t' + str(h) + '\t'  + str(bucket_number) + '\n')

output.close()
