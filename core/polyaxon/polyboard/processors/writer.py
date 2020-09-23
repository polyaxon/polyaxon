#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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

import os
import queue
import threading
import time

from typing import Dict, List, Union  # noqa

from polyaxon.polyboard.events import LoggedEventSpec, get_asset_path, get_event_path
from polyaxon.polyboard.events.paths import get_resource_path
from polyaxon.polyboard.events.schemas import LoggedEventListSpec
from polyaxon.polyboard.processors.gpu_processor import (
    can_log_gpu_resources,
    get_gpu_metrics,
)
from polyaxon.polyboard.processors.psutil_processor import (
    can_log_psutil_resources,
    get_psutils_metrics,
)
from polyaxon.utils.path_utils import check_or_create_path


class EventWriter:
    EVENTS_BACKEND = "events"
    RESOURCES_BACKEND = "resources"

    def __init__(self, run_path: str, backend: str):
        self._events_backend = backend
        self._run_path = run_path
        self._files = {}  # type: Dict[str, LoggedEventListSpec]
        self._closed = False

    def _get_event_path(self, kind: str, name: str) -> str:
        if self._events_backend == self.EVENTS_BACKEND:
            return os.path.join(
                self._run_path, self._events_backend, kind, "{}.plx".format(name)
            )
        if self._events_backend == self.RESOURCES_BACKEND:
            return os.path.join(
                self._run_path, self._events_backend, kind, "{}.plx".format(name)
            )
        raise ValueError("Unrecognized backend {}".format(self._events_backend))

    def _init_events(self, events_spec: LoggedEventListSpec):
        event_path = self._get_event_path(kind=events_spec.kind, name=events_spec.name)
        # Check if the file exists otherwise initialize
        if not os.path.exists(event_path):
            check_or_create_path(event_path, is_dir=False)
            with open(event_path, "w") as event_file:
                event_file.write(events_spec.get_csv_header())

    def _append_events(self, events_spec: LoggedEventListSpec):
        event_path = self._get_event_path(kind=events_spec.kind, name=events_spec.name)
        with open(event_path, "a") as event_file:
            event_file.write(events_spec.get_csv_events())

    def _events_to_files(self, events: List[LoggedEventSpec]):
        for event in events:
            file_name = "{}.{}".format(event.kind, event.name)
            if file_name in self._files:
                self._files[file_name].events.append(event.event)
            else:
                self._files[file_name] = LoggedEventListSpec(
                    kind=event.kind, name=event.name, events=[event.event]
                )
                self._init_events(self._files[file_name])

    def write(self, events: List[LoggedEventSpec]):
        if not events:
            return
        if isinstance(events, LoggedEventSpec):
            events = [events]
        self._events_to_files(events)

    def flush(self):
        for file_name in self._files:
            events_spec = self._files[file_name]
            if events_spec.events:
                self._append_events(events_spec)
            self._files[file_name].empty_events()

    def close(self):
        self.flush()
        self._closed = True

    @property
    def closed(self):
        return self._closed


class BaseFileWriter:
    """Writes `LoggedEventSpec` to event files.

    The `EventFileWriter` class creates a event files in the run path,
    and asynchronously writes Events to the files.
    """

    def __init__(self, run_path: str):
        self._run_path = run_path
        check_or_create_path(run_path, is_dir=True)

    @property
    def run_path(self):
        return self._run_path

    def add_event(self, event: LoggedEventSpec):
        if not isinstance(event, LoggedEventSpec):
            raise TypeError("Expected an LoggedEventSpec, " " but got %s" % type(event))
        self._async_writer.write(event)

    def add_events(self, events: List[LoggedEventSpec]):
        for e in events:
            if not isinstance(e, LoggedEventSpec):
                raise TypeError("Expected an LoggedEventSpec, " " but got %s" % type(e))
        self._async_writer.write(events)

    def flush(self):
        """Flushes the event files to disk.

        Call this method to make sure that all pending events have been
        written to disk.
        """
        self._async_writer.flush()

    def close(self):
        """Performs a final flush of the event files to disk, stops the
        write/flush worker and closes the files.

        Call this method when you do not need the writer anymore.
        """
        self._async_writer.close()


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
        """Enqueue the given event to be written asychronously."""
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
            self._event_queue, self._event_writer, flush_secs,
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
