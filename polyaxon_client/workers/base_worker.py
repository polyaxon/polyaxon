# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import atexit
import os
import threading


class BaseWorker(object):
    NAME = None

    def __init__(self):
        assert self.NAME, 'Worker class `{}` must have a valid name.'.format(
            self.__class__.__name__)
        self._lock = threading.Lock()
        self._thread = None
        self._thread_for_pid = None

    def is_alive(self):
        if self._thread_for_pid != os.getpid():
            return False
        return bool(self._thread and self._thread.is_alive())

    def is_running(self):
        if self.is_alive():
            return
        self.start()

    def start(self):
        self._lock.acquire()
        try:
            if not self.is_alive():
                self._thread = threading.Thread(target=self._target, name=self.NAME)
                self._thread.setDaemon(True)
                self._thread.start()
                self._thread_for_pid = os.getpid()
        finally:
            self._lock.release()
            atexit.register(self.atexit)

    def atexit(self):
        raise NotImplementedError('Worker must implement `atexit` function.')

    def _target(self):
        raise NotImplementedError('Worker must implement `target` function.')
