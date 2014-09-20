
from time import time


class Comment:
    """a class representation of a comment"""
    def __init__(self):
        # original comment fields
        self.id = None
        self.user_id = None
        self.user_name = None
        self.message = None
        self.created_time = None
        self.like_count = 0
        # analysis fields
        self.language = None

    def to_dict(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'user_name': self.user_name,
                'message': self.message,
                'created_time': self.created_time.isoformat(),
                'like_count': self.like_count,
                'language': self.language}


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
