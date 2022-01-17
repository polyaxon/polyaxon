#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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

from polyaxon.fs.watcher import FSWatcher
from polyaxon.logger import logger
from polyaxon.sidecar.ignore import IGNORE_FOLDERS


class SidecarThread(threading.Thread):
    """Thread that processes asynchronous writes for EventWriter."""

    def __init__(
        self, client, run_path: str, flush_secs: int = 10, sleep_secs: int = 1
    ):
        """Creates an EventWriterThread.

        Args:
          fs: The filesystem instance.
          fw: The filewatcher instance.
          flush_secs: How often, in seconds, to flush the
            pending file to disk.
        """
        threading.Thread.__init__(self)
        self.daemon = True
        self._client = client
        self._fw = FSWatcher()
        self._path = run_path
        self._flush_secs = flush_secs
        self._sleep_secs = sleep_secs
        self._next_flush_time = 0
        self._shutdown_signal = object()
        self._queue = queue.Queue(1)

    def _process(self):
        self._fw.init()
        self._fw.sync(self._path, exclude=IGNORE_FOLDERS)

        def get_path(_path: str, remove_basename: bool):
            if self._client.run_uuid in _path:
                _path = os.path.relpath(_path, self._client.run_uuid)
            if remove_basename:
                return os.path.split(_path)[0]
            return _path

        rm_files = self._fw.get_files_to_rm()
        logger.debug("rm_files {}".format(rm_files))
        for (_, subpath) in rm_files:
            self._client.delete_artifact(
                path=get_path(subpath, False),
            )

        rm_dirs = self._fw.get_dirs_to_rm()
        logger.debug("rm_dirs {}".format(rm_dirs))
        for (_, subpath) in rm_dirs:
            self._client.delete_artifacts(
                path=get_path(subpath, False),
            )

        put_files = self._fw.get_files_to_put()
        logger.debug("put_files {}".format(put_files))
        for (r_base_path, subpath) in put_files:
            try:
                self._client.upload_artifact(
                    filepath=os.path.join(r_base_path, subpath),
                    path=get_path(subpath, True),
                    show_progress=False,
                )
            except OSError as e:
                logger.warning("Could not perform delete operation, error: %", e)

    def close(self):
        self._queue.put(self._shutdown_signal)
        self.join()

    def run(self):
        # Wait for the queue until data appears, or until the next
        # time to flush the writer.
        # Invoke write If we have data.
        # If not, an empty queue exception will be raised and invoke writer flush.
        while True:
            try:
                if self._queue.get(False) is self._shutdown_signal:
                    self._process()
                    return
            except queue.Empty:
                pass

            now = time.time()
            if now > self._next_flush_time:
                self._process()
                self._next_flush_time = now + self._flush_secs
            time.sleep(self._sleep_secs)
