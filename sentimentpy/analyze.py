
class Analyzer:

   def __init__(self):
      return

   def analyze(self, comment):
      raise Exception("Method analyze() should be overrided by concrete subclasses")

   def finalize(self):
      raise Exception("Method finalize() should be overrided by concrete subclasses")


class AnalyzerManager:
    analyzers = []
    def __init__(self):
        return

    def add(self, other):
        self.analysers.append(other)

    def execute(self, comment):
        for analyser in self.analyzers:
            analyser.analyze(comment)