# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from six.moves.queue import Queue
from time import sleep, time

from polyaxon_client import settings
from polyaxon_client.logger import logger
from polyaxon_client.workers.base_worker import BaseWorker


class QueueWorker(BaseWorker):
    TIMEOUT_ATTEMPTS = 5
    QUEUE_SIZE = -1  # inf
    END_EVENT = object()
    NAME = 'polyaxon.QueueWorker'

    def __init__(self, timeout=None, queue_size=None):
        super(QueueWorker, self).__init__()
        self._queue = Queue(queue_size or self.QUEUE_SIZE)
        self._timeout = timeout if timeout is not None else settings.TIMEOUT

    def atexit(self):
        with self._lock:
            if not self.is_alive():
                return

            self._queue.put_nowait(self.END_EVENT)

            def timeout_join(timeout, queue):
                end = time() + timeout
                queue.all_tasks_done.acquire()
                try:
                    while queue.unfinished_tasks:
                        current_timeout = end - time()
                        if current_timeout <= 0:
                            # timed out
                            return False

                        queue.all_tasks_done.wait(timeout=current_timeout)

                    return True

                finally:
                    queue.all_tasks_done.release()

            # ensure wait
            timeout = min(settings.MIN_TIMEOUT, self._timeout / self.TIMEOUT_ATTEMPTS)
            if timeout_join(timeout=timeout, queue=self._queue):
                timeout = 0
            else:
                # Queue still has message, try another time
                size = self._queue.qsize()

                if not settings.IS_MANAGED:
                    print('Polyaxon %s is attempting to send %i pending messages' %
                          (self.NAME, size))
                    print('Waiting up to {} seconds'.format(self._timeout))
                    if os.name == 'nt':
                        print('Press Ctrl-Break to quit')
                    else:
                        print('Press Ctrl-C to quit')

            sleep(settings.MIN_TIMEOUT)  # Allow tasks to get executed
            while timeout > 0 and not timeout_join(timeout=timeout, queue=self._queue):
                timeout = min(timeout + self._timeout / self.TIMEOUT_ATTEMPTS,
                              self._timeout - timeout)

            size = self._queue.qsize()
            if size > 0:
                print('Polyaxon %s timed out and did not manage to send %i messages' %
                      (self.NAME, size))

            self._thread = None

    def stop(self, timeout=None):
        with self._lock:
            if self._thread:
                self._queue.put_nowait(self.END_EVENT)
                self._thread.join(timeout=timeout)
                self._thread = None
                self._thread_for_pid = None

    def queue(self, callback, *args, **kwargs):
        self.is_running()
        self._queue.put_nowait((callback, args, kwargs))

    def _target(self):
        while True:
            record = self._queue.get()
            try:
                if record is self.END_EVENT:
                    break
                callback, args, kwargs = record
                try:
                    callback(*args, **kwargs)
                except Exception:
                    logger.error('Failed processing job', exc_info=True)
            finally:
                self._queue.task_done()

            sleep(0)
