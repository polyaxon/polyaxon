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
import tarfile
import tempfile

from tests.utils import BaseTestCase

from polyaxon.utils.path_utils import (
    append_basename,
    create_project_tarfile,
    get_files_by_paths,
    get_files_in_path_context,
    get_path,
)


class TestFiles(BaseTestCase):
    def test_get_path(self):
        assert get_path("/foo", "bar") == "/foo/bar"

    def test_create_project_tarfile(self):
        files = ["tests/test_utils/__init__.py"]
        with create_project_tarfile(files, "project_name") as tar_file_name:
            assert os.path.exists(tar_file_name)
            with tarfile.open(tar_file_name) as tf:
                members = tf.getmembers()
                assert set([m.name for m in members]) == set(files)
        assert not os.path.exists(tar_file_name)

    def test_get_files_in_path_context_raises(self):
        filepaths = ["tests/test_utils/__init__.py"]
        with get_files_by_paths("repo", filepaths) as (files, files_size):
            assert len(filepaths) == len(files)

    def test_append_basename(self):
        assert append_basename("foo", "bar") == "foo/bar"
        assert append_basename("foo", "moo/bar") == "foo/bar"
        assert append_basename("/foo", "bar") == "/foo/bar"
        assert append_basename("/foo/moo", "bar") == "/foo/moo/bar"
        assert append_basename("/foo/moo", "boo/bar.txt") == "/foo/moo/bar.txt"

    def test_get_files_in_path_context(self):
        dirname = tempfile.mkdtemp()
        fpath1 = dirname + "/test1.txt"
        with open(fpath1, "w") as f:
            f.write("data1")

        fpath2 = dirname + "/test2.txt"
        with open(fpath2, "w") as f:
            f.write("data2")

        dirname2 = tempfile.mkdtemp(prefix=dirname + "/")
        fpath3 = dirname2 + "/test3.txt"
        with open(fpath3, "w") as f:
            f.write("data3")

        dirname3 = tempfile.mkdtemp(prefix=dirname + "/")
        fpath4 = dirname3 + "/test4.txt"
        with open(fpath4, "w") as f:
            f.write("data1")

        fpath5 = dirname3 + "/test5.txt"
        with open(fpath5, "w") as f:
            f.write("data2")

        dirname4 = tempfile.mkdtemp(prefix=dirname3 + "/")
        fpath6 = dirname4 + "/test6.txt"
        with open(fpath6, "w") as f:
            f.write("data3")

        with get_files_in_path_context(dirname) as files:
            assert len(files) == 6
            assert set(files) == {fpath1, fpath2, fpath3, fpath4, fpath5, fpath6}

        with get_files_in_path_context(
            dirname, exclude=[dirname3.split("/")[-1]]
        ) as files:
            assert len(files) == 3
            assert set(files) == {fpath1, fpath2, fpath3}
