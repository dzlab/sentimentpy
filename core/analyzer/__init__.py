__author__ = 'dzlab'


class Analyzer:

   def __init__(self):
      return

   def analyze(self, comment):
      raise Exception("Method analyze() should be overrided by concrete subclasses")

   def finalize(self):
      raise Exception("Method finalize() should be overrided by concrete subclasses")

