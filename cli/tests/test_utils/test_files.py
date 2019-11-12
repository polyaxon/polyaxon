#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# coding: utf-8
import os
import tarfile

from unittest import TestCase

from polyaxon.utils.files import create_tarfile, get_files_in_current_directory


class TestFiles(TestCase):
    def test_create_tarfile(self):
        files = ["tests/test_utils/__init__.py"]
        with create_tarfile(files, "project_name") as tar_file_name:
            assert os.path.exists(tar_file_name)
            with tarfile.open(tar_file_name) as tf:
                members = tf.getmembers()
                assert set([m.name for m in members]) == set(files)
        assert not os.path.exists(tar_file_name)

    def test_get_files_in_current_directory(self):
        filepaths = ["tests/test_utils/__init__.py"]
        with get_files_in_current_directory("repo", filepaths) as (files, files_size):
            assert len(filepaths) == len(files)
