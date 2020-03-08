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
import tempfile
import time

from tests.utils import BaseTestCase

from polyaxon.stores.local_store import LocalStore
from polyaxon.utils.date_utils import to_datetime


class TestLocalStore(BaseTestCase):
    def test_ls(self):
        store = LocalStore()

        dirname1 = tempfile.mkdtemp()
        dirname2 = tempfile.mkdtemp(prefix=dirname1 + "/")

        open(dirname1 + "/a", "w")
        open(dirname1 + "/b", "w")
        open(dirname2 + "/c", "w")

        full_response = {
            "files": [("a", 0), ("b", 0)],
            "dirs": [os.path.basename(dirname2)],
        }
        empty_response = {"dirs": [], "files": []}
        dir_response = {"dirs": [], "files": [("c", 0)]}

        assert store.ls(dirname1) == full_response
        assert store.ls(dirname1 + "/") == full_response
        assert store.ls(dirname1 + "/non-existent") == empty_response
        assert store.ls(dirname1 + "/non-existent/") == empty_response
        assert store.ls(dirname2) == dir_response
        assert store.ls(dirname2) == dir_response

    def test_delete(self):
        store = LocalStore()

        dirname1 = tempfile.mkdtemp()
        dirname2 = tempfile.mkdtemp(prefix=dirname1 + "/")

        open(dirname1 + "/a", "w")
        open(dirname1 + "/b", "w")
        open(dirname2 + "/c", "w")

        store.delete(dirname1 + "/a")
        assert store.ls(dirname1) == {
            "files": [("b", 0)],
            "dirs": [os.path.basename(dirname2)],
        }
        store.delete(dirname2)
        assert store.ls(dirname1) == {"files": [("b", 0)], "dirs": []}

    def test_upload(self):
        dirname = tempfile.mkdtemp()
        dirname2 = tempfile.mkdtemp()
        fpath = dirname + "/test.txt"
        open(fpath, "w")

        store = LocalStore()

        # Test without basename
        path2 = dirname2 + "/fo.txt"
        assert os.path.isfile(path2) is False
        store.upload_file(filename=fpath, path_to=path2, use_basename=False)
        assert os.path.isfile(path2) is True

        # Test with basename
        dirname2 = tempfile.mkdtemp()
        assert os.path.isfile(dirname2 + "/test.txt") is False
        store.upload_file(filename=fpath, path_to=dirname2, use_basename=True)
        assert os.path.isfile(dirname2 + "/test.txt") is True

    def test_download(self):
        dirname = tempfile.mkdtemp()
        dirname2 = tempfile.mkdtemp()
        fpath = dirname + "/test.txt"
        open(fpath, "w")

        store = LocalStore()

        # Test without basename
        path2 = dirname2 + "/fo.txt"
        assert os.path.isfile(path2) is False
        store.download_file(path_from=fpath, local_path=path2, use_basename=False)
        assert os.path.isfile(path2) is True

        # Test with basename
        dirname2 = tempfile.mkdtemp()
        assert os.path.isfile(dirname2 + "/test.txt") is False
        store.download_file(path_from=fpath, local_path=dirname2, use_basename=True)
        assert os.path.isfile(dirname2 + "/test.txt") is True

    def test_upload_dir(self):
        dirname1 = tempfile.mkdtemp()
        fpath1 = dirname1 + "/test1.txt"
        with open(fpath1, "w") as f:
            f.write("data1")

        fpath2 = dirname1 + "/test2.txt"
        with open(fpath2, "w") as f:
            f.write("data2")

        dirname2 = tempfile.mkdtemp(prefix=dirname1 + "/")
        fpath3 = dirname2 + "/test3.txt"
        with open(fpath3, "w") as f:
            f.write("data3")

        store = LocalStore()

        path_to = tempfile.mkdtemp()
        rel_path1 = dirname1.split("/")[-1]
        rel_path2 = dirname2.split("/")[-1]

        # Test without basename
        assert os.path.exists(os.path.join(path_to, "test1.txt")) is False
        assert os.path.exists(os.path.join(path_to, "test2.txt")) is False
        assert os.path.exists(os.path.join(path_to, rel_path2, "test3.txt")) is False
        store.upload_dir(dirname=dirname1, path_to=path_to, use_basename=False)
        assert os.path.exists(os.path.join(path_to, "test1.txt")) is True
        assert os.path.exists(os.path.join(path_to, "test2.txt")) is True
        assert os.path.exists(os.path.join(path_to, rel_path2, "test3.txt")) is True

        # Test with basename
        path_to = tempfile.mkdtemp()
        assert os.path.exists(os.path.join(path_to, rel_path1, "test1.txt")) is False
        assert os.path.exists(os.path.join(path_to, rel_path1, "test2.txt")) is False
        assert (
            os.path.exists(os.path.join(path_to, rel_path1, rel_path2, "test3.txt"))
            is False
        )
        store.upload_dir(dirname=dirname1, path_to=path_to, use_basename=True)
        assert os.path.exists(os.path.join(path_to, rel_path1, "test1.txt")) is True
        assert os.path.exists(os.path.join(path_to, rel_path1, "test2.txt")) is True
        assert (
            os.path.exists(os.path.join(path_to, rel_path1, rel_path2, "test3.txt"))
            is True
        )

    def test_upload_dir_with_last_time(self):
        dirname1 = tempfile.mkdtemp()
        fpath1 = dirname1 + "/test1.txt"
        with open(fpath1, "w") as f:
            f.write("data1")

        fpath2 = dirname1 + "/test2.txt"
        with open(fpath2, "w") as f:
            f.write("data2")

        last_time = to_datetime(os.stat(fpath2).st_mtime)
        time.sleep(0.1)

        dirname2 = tempfile.mkdtemp(prefix=dirname1 + "/")
        fpath3 = dirname2 + "/test3.txt"
        with open(fpath3, "w") as f:
            f.write("data3")

        store = LocalStore()

        path_to = tempfile.mkdtemp()
        rel_path1 = dirname1.split("/")[-1]
        rel_path2 = dirname2.split("/")[-1]

        # Test without basename
        assert os.path.exists(os.path.join(path_to, "test1.txt")) is False
        assert os.path.exists(os.path.join(path_to, "test2.txt")) is False
        assert os.path.exists(os.path.join(path_to, rel_path2, "test3.txt")) is False
        store.upload_dir(
            dirname=dirname1, path_to=path_to, use_basename=False, last_time=last_time
        )
        assert os.path.exists(os.path.join(path_to, "test1.txt")) is False
        assert os.path.exists(os.path.join(path_to, "test2.txt")) is False
        assert os.path.exists(os.path.join(path_to, rel_path2, "test3.txt")) is True

        # Test with basename
        path_to = tempfile.mkdtemp()
        assert os.path.exists(os.path.join(path_to, rel_path1, "test1.txt")) is False
        assert os.path.exists(os.path.join(path_to, rel_path1, "test2.txt")) is False
        assert (
            os.path.exists(os.path.join(path_to, rel_path1, rel_path2, "test3.txt"))
            is False
        )
        store.upload_dir(
            dirname=dirname1, path_to=path_to, use_basename=True, last_time=last_time
        )
        assert os.path.exists(os.path.join(path_to, "test1.txt")) is False
        assert os.path.exists(os.path.join(path_to, "test2.txt")) is False
        assert (
            os.path.exists(os.path.join(path_to, rel_path1, rel_path2, "test3.txt"))
            is True
        )

    def test_download_dir(self):
        dirname1 = tempfile.mkdtemp()
        fpath1 = dirname1 + "/test1.txt"
        with open(fpath1, "w") as f:
            f.write("data1")

        fpath2 = dirname1 + "/test2.txt"
        with open(fpath2, "w") as f:
            f.write("data2")

        dirname2 = tempfile.mkdtemp(prefix=dirname1 + "/")
        fpath3 = dirname2 + "/test3.txt"
        with open(fpath3, "w") as f:
            f.write("data3")

        store = LocalStore()

        path_to = tempfile.mkdtemp()
        rel_path1 = dirname1.split("/")[-1]
        rel_path2 = dirname2.split("/")[-1]

        # Test without basename
        assert os.path.exists(os.path.join(path_to, "test1.txt")) is False
        assert os.path.exists(os.path.join(path_to, "test2.txt")) is False
        assert os.path.exists(os.path.join(path_to, rel_path2, "test3.txt")) is False
        store.download_dir(path_from=dirname1, local_path=path_to, use_basename=False)
        assert os.path.exists(os.path.join(path_to, "test1.txt")) is True
        assert os.path.exists(os.path.join(path_to, "test2.txt")) is True
        assert os.path.exists(os.path.join(path_to, rel_path2, "test3.txt")) is True

        # Test with basename
        path_to = tempfile.mkdtemp()
        assert os.path.exists(os.path.join(path_to, rel_path1, "test1.txt")) is False
        assert os.path.exists(os.path.join(path_to, rel_path1, "test2.txt")) is False
        assert (
            os.path.exists(os.path.join(path_to, rel_path1, rel_path2, "test3.txt"))
            is False
        )
        store.download_dir(path_from=dirname1, local_path=path_to, use_basename=True)
        assert os.path.exists(os.path.join(path_to, rel_path1, "test1.txt")) is True
        assert os.path.exists(os.path.join(path_to, rel_path1, "test2.txt")) is True
        assert (
            os.path.exists(os.path.join(path_to, rel_path1, rel_path2, "test3.txt"))
            is True
        )
