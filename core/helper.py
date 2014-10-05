import threading
from time import time
from guess_language import guess_language


guess_lock = threading.Lock()


def guess_language_thread_safe(text):
    with guess_lock:
        return guess_language(text)


class WatchTime:
    def __init__(self):
        self.start_time = 0
        self.stop_time = 0
        self.total_time = 0

    def reset(self):
        self.start_time = 0
        self.stop_time = 0
        self.total_time = 0

    def start(self):
        self.start_time = time()
        self.stop_time = self.start_time

    def stop(self):
        self.stop_time = time()
        self.total_time += (self.stop_time - self.start_time)

    def elapsed(self):
        return self.stop_time - self.start_time

    def total(self):
        return self.total_time


def trace_calls(frame, event, arg):
    if event != 'call':
        return
    co = frame.f_code
    func_name = co.co_name
    if func_name == 'write':
        # Ignore write() calls from print statements
        return
    func_line_no = frame.f_lineno
    func_filename = co.co_filename
    caller = frame.f_back
    caller_line_no = caller.f_lineno
    caller_filename = caller.f_code.co_filename
    print 'Call to %s on line %s of %s from line %s of %s' % (func_name, func_line_no, func_filename, caller_line_no, caller_filename)
    return
