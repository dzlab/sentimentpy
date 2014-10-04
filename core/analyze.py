
import logging
from Queue import Queue
from threading import Thread, current_thread
from core.utils.thread_pool import ThreadPool


class AnalyzerWorker(Thread):
    """Thread performing analysis of comments"""
    logger = logging.getLogger('AnalyzerWorker')

    def __init__(self, analyzer, comments_queue):
        Thread.__init__(self)
        self.comments_queue = comments_queue
        self.analyzer = analyzer
        self.daemon = True
        self.start()

    def run(self):
        while True:
            comment = self.comments_queue.get()
            self.analyzer.analyze(comment)
            self.comments_queue.task_done()
            self.logger.debug('%d comments remaining to process by %s' % (self.comments_queue.qsize(), self.analyzer))

    def finalize(self):
        self.analyzer.finalize()
        AnalyzerWorker.logger.debug("%s successfully finalized analyzer '%s'" % (self.name, self.analyzer))


class AnalyzerManager:
    logger = logging.getLogger('AnalyzerManager')

    def __init__(self, size=1000):
        self.size = size
        self.workers = []

    def register(self, analyzer):
        """Register an analyzer"""
        self.workers.append(AnalyzerWorker(analyzer, Queue(self.size)))

    def process(self, comment):
        if not comment:
            self.logger.info("Cannot process a non valid comment")
            return
        for worker in self.workers:
            # if worker's queue is full block otherwise enqueue without blocking
            if worker.comments_queue.full():
                worker.comments_queue.put(comment)
            else:
                worker.comments_queue.put_nowait(comment)

    def finalize(self):
        self.logger.debug("Finalizing all analysis")
        for worker in self.workers:
            worker.comments_queue.join()
            worker.finalize()

    @staticmethod
    def execute(analyzer, comment):
        AnalyzerManager.logger.info("%s analyzing %s with %s" % (current_thread(), comment, analyzer))
        analyzer.analyze(comment)