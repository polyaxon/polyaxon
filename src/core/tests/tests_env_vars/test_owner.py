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

from polyaxon.env_vars.getters import get_entity_full_name, get_entity_info
from polyaxon.env_vars.getters.owner_entity import resolve_entity_info
from polyaxon.exceptions import PolyaxonClientException, PolyaxonSchemaError
from tests.utils import BaseTestCase


class TestOwnerEnvVars(BaseTestCase):
    def test_get_entity_full_name(self):
        assert get_entity_full_name(None) is None
        assert get_entity_full_name("owner", None) is None
        assert get_entity_full_name("owner", "entity") == "owner/entity"

    def test_get_entity_info(self):
        with self.assertRaises(PolyaxonSchemaError):
            get_entity_info(None)

        with self.assertRaises(PolyaxonSchemaError):
            get_entity_info("")

        with self.assertRaises(PolyaxonSchemaError):
            get_entity_info("foo.bar.moo")

        with self.assertRaises(PolyaxonSchemaError):
            get_entity_info("foo/bar/moo")

        assert get_entity_info("entity") == (None, "entity")
        assert get_entity_info("owner.entity") == ("owner", "entity")
        assert get_entity_info("owner/entity") == ("owner", "entity")

    def test_resolve_entity_info(self):
        with self.assertRaises(PolyaxonClientException):
            resolve_entity_info("", "")

        with self.assertRaises(PolyaxonClientException):
            resolve_entity_info("", "test")

        with self.assertRaises(PolyaxonClientException):
            resolve_entity_info(None, None)

        with self.assertRaises(PolyaxonSchemaError):
            resolve_entity_info("owner.entity.test", "")

        with self.assertRaises(PolyaxonSchemaError):
            resolve_entity_info("owner/entity/test", "")

        assert resolve_entity_info("owner.entity", "project") == ("owner", "entity")
