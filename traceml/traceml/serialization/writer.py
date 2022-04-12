#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import queue
import threading
import time

from typing import List, Union

from polyaxon.utils.path_utils import check_or_create_path
from traceml.events import LoggedEventSpec, get_asset_path, get_event_path
from traceml.events.paths import get_resource_path
from traceml.processors.gpu_processor import can_log_gpu_resources, get_gpu_metrics
from traceml.processors.psutil_processor import (
    can_log_psutil_resources,
    get_psutils_metrics,
)
from traceml.serialization.base import BaseFileWriter, EventWriter


class EventFileWriter(BaseFileWriter):
    def __init__(self, run_path: str, max_queue_size: int = 20, flush_secs: int = 10):
        """Creates a `EventFileWriter`.

        Args:
          run_path: A string. Directory where events files will be written.
          max_queue_size: Integer. Size of the queue for pending events and summaries.
          flush_secs: Number. How often, in seconds, to flush the
            pending events and summaries to disk.
        """
        super().__init__(run_path=run_path)

        check_or_create_path(get_event_path(run_path), is_dir=True)
        check_or_create_path(get_asset_path(run_path), is_dir=True)

        self._async_writer = EventAsyncManager(
            EventWriter(self._run_path, backend=EventWriter.EVENTS_BACKEND),
            max_queue_size,
            flush_secs,
        )


class ResourceFileWriter(BaseFileWriter):
    def __init__(self, run_path: str, max_queue_size: int = 20, flush_secs: int = 10):
        """Creates a `ResourceFileWriter`.

        Args:
          run_path: A string. Directory where events files will be written.
          max_queue_size: Integer. Size of the queue for pending events and summaries.
          flush_secs: Number. How often, in seconds, to flush the
            pending events and summaries to disk.
        """
        super().__init__(run_path=run_path)

        check_or_create_path(get_resource_path(run_path), is_dir=True)

        self._async_writer = ResourceAsyncManager(
            EventWriter(self._run_path, backend=EventWriter.RESOURCES_BACKEND),
            max_queue_size,
            flush_secs,
        )


class BaseAsyncManager:
    """Base manager for writing events to files by name by event kind."""

    def __init__(self, event_writer: EventWriter, max_queue_size: int = 20):
        """Writes events json spec to files asynchronously. An instance of this class
        holds a queue to keep the incoming data temporarily. Data passed to the
        `write` function will be put to the queue and the function returns
        immediately. This class also maintains a thread to write data in the
        queue to disk.

        Args:
            event_writer: A EventWriter instance
            max_queue_size: Integer. Size of the queue for pending bytestrings.
            flush_secs: Number. How often, in seconds, to flush the
                pending bytestrings to disk.
        """
        self._event_writer = event_writer
        self._closed = False
        self._event_queue = queue.Queue(max_queue_size)
        self._lock = threading.Lock()
        self._worker = None

    def write(self, event: Union[LoggedEventSpec, List[LoggedEventSpec]]):
        """Enqueue the given event to be written asynchronously."""
        with self._lock:
            if self._closed:
                raise IOError("Writer is closed")
            self._event_queue.put(event)

    def flush(self):
        """Write all the enqueued events before this flush call to disk.

        Block until all the above events are written.
        """
        with self._lock:
            if self._closed:
                raise IOError("Writer is closed")
            self._event_queue.join()
            self._event_writer.flush()

    def close(self):
        """Closes the underlying writer, flushing any pending writes first."""
        if not self._closed:
            with self._lock:
                if not self._closed:
                    self._closed = True
                    self._worker.stop()
                    self._event_writer.flush()
                    self._event_writer.close()


class EventAsyncManager(BaseAsyncManager):
    """Writes events to files by name by event kind."""

    def __init__(
        self, event_writer: EventWriter, max_queue_size: int = 20, flush_secs: int = 10
    ):
        super().__init__(event_writer=event_writer, max_queue_size=max_queue_size)
        self._worker = EventWriterThread(
            self._event_queue, self._event_writer, flush_secs
        )
        self._worker.start()


class EventWriterThread(threading.Thread):
    """Thread that processes asynchronous writes for EventWriter."""

    def __init__(self, event_queue, event_writer: EventWriter, flush_secs: int):
        """Creates an EventWriterThread.

        Args:
          event_queue: A Queue from which to dequeue data.
          event_writer: An instance of EventWriter.
          flush_secs: How often, in seconds, to flush the
            pending file to disk.
        """
        threading.Thread.__init__(self)
        self.daemon = True
        self._event_queue = event_queue
        self._event_writer = event_writer
        self._flush_secs = flush_secs
        # The first data will be flushed immediately.
        self._next_flush_time = 0
        self._has_pending_data = False
        self._shutdown_signal = object()

    def stop(self):
        self._event_queue.put(self._shutdown_signal)
        self.join()

    def run(self):
        # Wait for the queue until data appears, or until the next
        # time to flush the writer.
        # Invoke write If we have data.
        # If not, an empty queue exception will be raised and invoke writer flush.
        while True:
            now = time.time()
            queue_wait_duration = self._next_flush_time - now
            data = None
            try:
                if queue_wait_duration > 0:
                    data = self._event_queue.get(True, queue_wait_duration)
                else:
                    data = self._event_queue.get(False)

                if data is self._shutdown_signal:
                    return
                self._event_writer.write(data)
                self._has_pending_data = True
            except queue.Empty:
                pass
            finally:
                if data:
                    self._event_queue.task_done()

            now = time.time()
            if now > self._next_flush_time:
                if self._has_pending_data:
                    # Small optimization - if there are no pending data,
                    # there's no need to flush.
                    self._event_writer.flush()
                    self._has_pending_data = False
                # Do it again in flush_secs.
                self._next_flush_time = now + self._flush_secs


class ResourceAsyncManager(BaseAsyncManager):
    """Writes resource events to files by name by event kind."""

    def __init__(
        self, event_writer: EventWriter, max_queue_size: int = 20, flush_secs: int = 10
    ):
        super().__init__(event_writer=event_writer, max_queue_size=max_queue_size)
        self._worker = ResourceWriterThread(
            self._event_queue,
            self._event_writer,
            flush_secs,
        )
        self._worker.start()


class ResourceWriterThread(EventWriterThread):
    """Thread that processes periodic resources (cpu, gpu, memory) writes for EventWriter."""

    def __init__(self, event_queue, event_writer: EventWriter, flush_secs: int):
        super().__init__(
            event_queue=event_queue, event_writer=event_writer, flush_secs=flush_secs
        )
        self._log_psutil_resources = can_log_psutil_resources()
        self._log_gpu_resources = can_log_gpu_resources()

    def run(self):
        # Wait for flush time to invoke the writer.
        while True:
            now = time.time()
            queue_wait_duration = self._next_flush_time - now
            data = None
            try:
                if queue_wait_duration > 0:
                    data = self._event_queue.get(True, queue_wait_duration)
                else:
                    data = self._event_queue.get(False)

                if data is self._shutdown_signal:
                    return
                self._event_writer.write(data)
                self._has_pending_data = True
            except queue.Empty:
                pass
            finally:
                if data:
                    self._event_queue.task_done()

            now = time.time()
            if now > self._next_flush_time:
                data = []
                if self._log_psutil_resources:
                    try:
                        data += get_psutils_metrics()
                    except Exception:
                        pass
                try:
                    data += get_gpu_metrics()
                except Exception:
                    pass
                if data:
                    self._event_writer.write(data)
                    self._event_writer.flush()
                self._next_flush_time = now + self._flush_secs
