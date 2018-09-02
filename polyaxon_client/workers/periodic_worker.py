# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import threading

from polyaxon_client.workers.base_worker import BaseWorker


class PeriodicWorker(BaseWorker):
    NAME = 'polyaxon.PeriodicWorker'

    def __init__(self, interval, callback, *args, **kwargs):
        super(PeriodicWorker, self).__init__()
        self._interval = interval
        self._finished = threading.Event()
        self._callback = callback
        self._args = args
        self._kwargs = kwargs

    def stop(self):
        with self._lock:
            if self._thread:
                self._finished.set()
                self._thread.join()
                self._thread = None
                self._thread_for_pid = None

    def atexit(self):
        self.stop()

    def _target(self):
        while True:
            if not self.is_alive() or self._finished.isSet():
                break
            self._finished.wait(self._interval)
            self._callback(*self._args, **self._kwargs)
