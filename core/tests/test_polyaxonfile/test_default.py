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

import pytest
import tempfile

from polyaxon.polyaxonfile import (
    DEFAULT_POLYAXON_FILE_EXTENSION,
    DEFAULT_POLYAXON_FILE_NAME,
    check_default_path,
)
from tests.utils import BaseTestCase


@pytest.mark.polyaxonfile_mark
class TestDefaultFile(BaseTestCase):
    def test_default_not_found(self):
        path = tempfile.mkdtemp()
        assert check_default_path(path=path) is None

    def test_polyaxon_found(self):
        def create_file(path, filename, ext):
            fpath = "{}/{}.{}".format(path, filename, ext)
            open(fpath, "w")

        for filename in DEFAULT_POLYAXON_FILE_NAME:
            for ext in DEFAULT_POLYAXON_FILE_EXTENSION:
                path = tempfile.mkdtemp()
                create_file(path, filename, ext)
                assert check_default_path(path=path)
