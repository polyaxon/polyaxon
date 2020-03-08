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

import pytest

from tests.utils import BaseTestCase

from polyaxon.proxies.generators import (
    generate_api_conf,
    generate_gateway_conf,
    generate_streams_conf,
)


@pytest.mark.proxies_mark
class TestGenerate(BaseTestCase):
    SET_PROXIES_SETTINGS = True

    def test_generate_api_conf(self):
        tmp_dir = tempfile.mkdtemp()
        assert os.listdir(tmp_dir) == []
        generate_api_conf(path=tmp_dir)
        assert set(os.listdir(tmp_dir)) == {"polyaxon.main.conf", "polyaxon.base.conf"}

    def test_generate_gateway_conf(self):
        tmp_dir = tempfile.mkdtemp()
        assert os.listdir(tmp_dir) == []
        generate_gateway_conf(path=tmp_dir)
        assert set(os.listdir(tmp_dir)) == {
            "polyaxon.main.conf",
            "polyaxon.base.conf",
            "polyaxon.redirect.conf",
        }

    def test_generate_streams_conf(self):
        tmp_dir = tempfile.mkdtemp()
        assert os.listdir(tmp_dir) == []
        generate_streams_conf(path=tmp_dir)
        assert set(os.listdir(tmp_dir)) == {"polyaxon.main.conf", "polyaxon.base.conf"}
