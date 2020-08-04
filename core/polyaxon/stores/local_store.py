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
import shutil

from concurrent import futures
from typing import List

from polyaxon.logger import logger
from polyaxon.stores.base_store import StoreMixin
from polyaxon.utils.date_utils import file_modified_since
from polyaxon.utils.path_utils import (
    append_basename,
    check_or_create_path,
    copy_file,
    get_files_in_path_context,
)


class LocalStore(StoreMixin):
    """
    Local filesystem store.

    This store is no op or moving data from one location to another,
    since all data is accessible through the filesystem.
    """

    @staticmethod
    def _list(path, check, abs_path=False):
        """
        List all entities directly under 'dir_name' that satisfy 'filter_func'

        Args:
            path: path where to start search
            check: function to check whether or not to include the results.
            abs_path: If True will return results with abs path.

        Returns:
            list of all files or directories under the path after the check.
        """
        if not os.path.isdir(path):
            logger.warning("Invalid parent directory '%s'" % path)
            return []
        matches = sorted([x for x in os.listdir(path) if check(os.path.join(path, x))])
        return [os.path.join(path, m) for m in matches] if abs_path else matches

    def ls(self, path):
        return self.list(path=path)

    def list(self, path, abs_path=False):
        def list_dirs():
            return self._list(path, os.path.isdir, abs_path)

        def list_files():
            matches = self._list(path, os.path.isfile, abs_path)
            if abs_path:
                return [(f, os.path.getsize(f)) for f in matches]
            return [(f, os.path.getsize(os.path.join(path, f))) for f in matches]

        return {"dirs": list_dirs(), "files": list_files()}

    def download_file(self, path_from, local_path, use_basename=True, **kwargs):
        local_path = os.path.abspath(local_path)

        if use_basename:
            local_path = append_basename(local_path, path_from)

        if local_path == path_from:
            return

        check_or_create_path(local_path, is_dir=False)
        if os.path.exists(path_from) and os.path.isfile(path_from):
            shutil.copy(path_from, local_path)

    def upload_file(self, filename, path_to, use_basename=True, **kwargs):
        copy_file(filename=filename, path_to=path_to, use_basename=use_basename)

    def upload_dir(
        self,
        dirname,
        path_to,
        use_basename=True,
        workers=0,
        last_time=None,
        exclude: List[str] = None,
    ):
        if use_basename:
            path_to = append_basename(path_to, dirname)

        if dirname == path_to:
            return

        check_or_create_path(path_to, is_dir=True)
        pool, future_results = self.init_pool(workers)

        # Turn the path to absolute paths
        dirname = os.path.abspath(dirname)
        with get_files_in_path_context(dirname, exclude=exclude) as files:
            for f in files:

                # If last time is provided we check if we should re-upload the file
                if last_time and not file_modified_since(
                    filepath=f, last_time=last_time
                ):
                    continue

                file_blob = os.path.join(path_to, os.path.relpath(f, dirname))
                future_results = self.submit_pool(
                    workers=workers,
                    pool=pool,
                    future_results=future_results,
                    fn=self.upload_file,
                    filename=f,
                    path_to=file_blob,
                    use_basename=False,
                )

        if workers:
            futures.wait(future_results)
            self.close_pool(pool=pool)

    def download_dir(
        self, path_from, local_path, use_basename=True, workers=0, **kwargs
    ):
        self.upload_dir(
            dirname=path_from,
            path_to=local_path,
            use_basename=use_basename,
            workers=workers,
            **kwargs
        )

    def delete_file(self, path, **kwargs):
        os.remove(path)

    def delete(self, path, **kwargs):
        if not os.path.exists(path):
            return
        try:
            if os.path.isfile(path):
                os.remove(path)
            else:
                shutil.rmtree(path)
        except OSError:
            logger.warning("Could not delete path `%s`", path)
