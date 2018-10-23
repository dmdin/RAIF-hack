import sys
import threading
import queue


class CarefulThread(threading.Thread):
    def __init__(self, bucket, update, target, args=None, kwargs=None):
        threading.Thread.__init__(self)
        self.bucket = bucket  # type: queue.Queue
        self._target = target
        self._update = update

        if args is None:
            self._args = ()
        else:
            self._args = args
        if kwargs is None:
            self._kwargs = {}
        else:
            self._kwargs = kwargs


    def run(self):
        try:
            self._target(*self._args, **self._kwargs)
        except Exception as e:
            self.bucket.put([sys.exc_info(), self._update])
