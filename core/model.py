__author__ = 'dzlab'

import threading
from dateutil import parser


class Comment:
    """a class representation of a comment"""
    lock = threading.RLock()

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

    def set_language(self, language=None):
        with Comment.lock:
            self.language = language

    def to_dict(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'user_name': self.user_name,
                'message': self.message,
                'created_time': self.created_time,#.isoformat(),
                'like_count': self.like_count,
                'language': self.language}

    @staticmethod
    def from_dict(**entries):
        """Convert a dictionary to a comment class
        :param entries Dictionary
        :return class:Struct"""
        c = Comment()
        c.id = entries['id']
        c.user_id = entries['user_id']
        c.user_name = entries['user_name']
        c.message = entries['message']
        c.created_time = entries['created_time']
        c.like_count = entries['like_count']
        c.language = entries['language']
        if c.created_time:
            c.created_time = parser.parse(c.created_time)
        return c


class Struct(object):
    def __init__(self, **entries):
        """Convert a dictionary to a class
        @:param adict Dictionary
        """
        self.__dict__.update(entries)
        for k, v in entries.items():
            if isinstance(v, dict):
                self.__dict__[k] = Struct(v)

    @staticmethod
    def to_object(**entries):
        """Convert a dictionary to a comment class
        :param entries Dictionary
        :return class:Struct"""
        return Struct(**entries)
