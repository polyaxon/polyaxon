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

from polyaxon.config_reader.manager import ConfigManager
from polyaxon.exceptions import PolyaxonSchemaError
from polyaxon.schemas.types import V1AuthType, V1UriType
from tests.utils import BaseTestCase


class TestConfigManager(BaseTestCase):
    def setUp(self):
        super().setUp()
        os.environ["FOO_BAR_KEY"] = "foo_bar"
        self.config = ConfigManager.read_configs(
            [os.environ, "tests/fixtures/parsing/configs/config_tests.json"]
        )

    def test_get_from_os_env(self):
        assert self.config.get_string("FOO_BAR_KEY") == "foo_bar"

    def test_reading_invalid_json_config_raises_error(self):
        with self.assertRaises(PolyaxonSchemaError):
            ConfigManager.read_configs(
                ["tests/fixtures/parsing/configs/invalid_config_tests.json"]
            )

    def test_reading_invalid_yaml_config_raises_error(self):
        with self.assertRaises(PolyaxonSchemaError):
            ConfigManager.read_configs(
                ["tests/fixtures/parsing/configs/invalid_config_tests.yaml"]
            )

    def test_get_boolean(self):
        value = self.config.get_boolean("bool_key_1")
        self.assertEqual(value, True)

        value = self.config.get_boolean("bool_key_2")
        self.assertEqual(value, True)

        value = self.config.get_boolean("bool_key_3")
        self.assertEqual(value, False)

        value = self.config.get_boolean("bool_key_4")
        self.assertEqual(value, False)

        value = self.config.get_boolean("bool_list_key_1", is_list=True)
        self.assertEqual(value, [False, False, True, True, True, False])

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_boolean("bool_error_key_1")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_boolean("bool_error_key_2")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_boolean("bool_error_key_3")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_boolean("bool_error_key_4")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_boolean("bool_error_key_5")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_boolean("bool_list_key_1")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_boolean("bool_list_error_key_2", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_boolean("bool_list_error_key_1", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_boolean("bool_key_1", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_boolean("bool_key_2", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_boolean("bool_non_existing_key")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_boolean("bool_non_existing_key", is_list=True)

        self.assertEqual(
            self.config.get_boolean("bool_non_existing_key", is_optional=True), None
        )
        self.assertEqual(
            self.config.get_boolean(
                "bool_non_existing_key", is_optional=True, default=True
            ),
            True,
        )

        self.assertEqual(
            self.config.get_boolean(
                "bool_non_existing_key", is_list=True, is_optional=True
            ),
            None,
        )
        self.assertEqual(
            self.config.get_boolean(
                "bool_non_existing_key",
                is_list=True,
                is_optional=True,
                default=[True, False],
            ),
            [True, False],
        )

    def test_get_int(self):
        value = self.config.get_int("int_key_1")
        self.assertEqual(value, 123)

        value = self.config.get_int("int_key_2")
        self.assertEqual(value, 123)

        value = self.config.get_int("int_list_key_1", is_list=True)
        self.assertEqual(value, [123, 124, 125, 125])

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_int("int_error_key_1")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_int("int_error_key_2")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_int("int_error_key_3")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_int("int_list_key_1")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_int("int_list_error_key_1", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_int("int_list_error_key_2", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_int("int_list_error_key_3", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_int("int_key_1", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_int("int_key_2", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_int("int_non_existing_key")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_int("int_non_existing_key", is_list=True)

        self.assertEqual(
            self.config.get_int("int_non_existing_key", is_optional=True), None
        )
        self.assertEqual(
            self.config.get_int("int_non_existing_key", is_optional=True, default=34),
            34,
        )

        self.assertEqual(
            self.config.get_int("int_non_existing_key", is_list=True, is_optional=True),
            None,
        )
        self.assertEqual(
            self.config.get_int(
                "int_non_existing_key", is_list=True, is_optional=True, default=[34, 1]
            ),
            [34, 1],
        )

    def test_get_float(self):
        value = self.config.get_float("float_key_1")
        self.assertEqual(value, 1.23)

        value = self.config.get_float("float_key_2")
        self.assertEqual(value, 1.23)

        value = self.config.get_float("float_key_3")
        self.assertEqual(value, 123)

        value = self.config.get_float("float_key_4")
        self.assertEqual(value, 123.0)

        value = self.config.get_float("float_list_key_1", is_list=True)
        self.assertEqual(value, [1.23, 13.3, 4.4, 555.0, 66.0])

        value = self.config.get_float("float_list_key_2", is_list=True)
        self.assertEqual(value, [1.23, 13.3, 66])

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_float("float_error_key_1")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_float("float_error_key_2")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_float("float_error_key_3")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_float("float_list_key_1")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_float("float_list_error_key_2", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_float("float_list_error_key_3", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_float("float_key_1", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_float("float_key_2", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_float("float_non_existing_key")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_float("float_non_existing_key", is_list=True)

        self.assertEqual(
            self.config.get_float("float_non_existing_key", is_optional=True), None
        )
        self.assertEqual(
            self.config.get_float(
                "float_non_existing_key", is_optional=True, default=3.4
            ),
            3.4,
        )

        self.assertEqual(
            self.config.get_float(
                "float_non_existing_key", is_list=True, is_optional=True
            ),
            None,
        )
        self.assertEqual(
            self.config.get_float(
                "float_non_existing_key",
                is_list=True,
                is_optional=True,
                default=[3.4, 1.2],
            ),
            [3.4, 1.2],
        )

    def test_get_string(self):
        value = self.config.get_string("string_key_1")
        self.assertEqual(value, "123")

        value = self.config.get_string("string_key_2")
        self.assertEqual(value, "1.23")

        value = self.config.get_string("string_key_3")
        self.assertEqual(value, "foo")

        value = self.config.get_string("string_key_4")
        self.assertEqual(value, "")

        value = self.config.get_string("string_list_key_1", is_list=True)
        self.assertEqual(value, ["123", "1.23", "foo", ""])

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_string("string_error_key_1")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_string("string_error_key_2")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_string("string_error_key_3")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_string("string_error_key_4")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_string("string_list_key_1")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_string("string_list_error_key_1", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_string("string_list_error_key_2", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_string("string_list_error_key_3", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_string("string_list_error_key_4", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_string("string_key_3", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_string("string_key_4", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_string("string_non_existing_key")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_string("string_non_existing_key", is_list=True)

        self.assertEqual(
            self.config.get_string("string_non_existing_key", is_optional=True), None
        )
        self.assertEqual(
            self.config.get_string(
                "string_non_existing_key", is_optional=True, default="foo"
            ),
            "foo",
        )

        self.assertEqual(
            self.config.get_string(
                "string_non_existing_key", is_list=True, is_optional=True
            ),
            None,
        )
        self.assertEqual(
            self.config.get_string(
                "string_non_existing_key",
                is_list=True,
                is_optional=True,
                default=["foo", "bar"],
            ),
            ["foo", "bar"],
        )

    def test_get_dict(self):
        value = self.config.get_dict("dict_key_1")
        self.assertEqual(value, {"key1": "foo", "key2": 2, "key3": False, "key4": "1"})

        value = self.config.get_dict("dict_list_key_1", is_list=True)
        self.assertEqual(
            value,
            [
                {"key1": "foo", "key2": 2, "key3": False, "key4": "1"},
                {"key3": True, "key4": "2"},
                {"key1": False, "key2": "3"},
            ],
        )

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_dict("dict_error_key_1")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_dict("dict_error_key_2")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_dict("dict_error_key_3")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_dict("dict_error_key_4")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_dict("dict_list_key_1")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_dict("dict_list_error_key_1", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_dict("dict_list_error_key_2", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_dict("dict_list_error_key_3", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_dict("dict_list_error_key_4", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_dict("dict_key_1", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_dict("dict_non_existing_key")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_dict("dict_non_existing_key", is_list=True)

        self.assertEqual(
            self.config.get_dict("dict_non_existing_key", is_optional=True), None
        )
        self.assertEqual(
            self.config.get_dict(
                "dict_non_existing_key", is_optional=True, default={"foo": "bar"}
            ),
            {"foo": "bar"},
        )

        self.assertEqual(
            self.config.get_dict(
                "dict_non_existing_key", is_list=True, is_optional=True
            ),
            None,
        )
        self.assertEqual(
            self.config.get_dict(
                "dict_non_existing_key",
                is_list=True,
                is_optional=True,
                default=[{"foo": "bar"}, {"foo": "boo"}],
            ),
            [{"foo": "bar"}, {"foo": "boo"}],
        )

    def test_get_uri(self):
        value = self.config.get_uri("uri_key_1")
        self.assertEqual(value, V1UriType("user", "pass", "siteweb.ca"))

        value = self.config.get_uri("uri_key_2")
        self.assertEqual(value, V1UriType("user2", "pass", "localhost:8080"))

        value = self.config.get_uri("uri_key_3")
        self.assertEqual(value, V1UriType("user2", "pass", "https://quay.io"))

        value = self.config.get_uri("uri_list_key_1", is_list=True)
        self.assertEqual(
            value,
            [
                V1UriType("user", "pass", "siteweb.ca"),
                V1UriType("user2", "pass", "localhost:8080"),
                V1UriType("user2", "pass", "https://quay.io"),
            ],
        )

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_uri("uri_error_key_1")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_uri("uri_error_key_2")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_uri("uri_error_key_3")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_uri("uri_error_key_4")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_uri("uri_list_key_1")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_uri("uri_list_error_key_1", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_uri("uri_list_error_key_2", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_uri("uri_list_error_key_3", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_uri("uri_list_error_key_4", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_uri("uri_key_1", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_uri("uri_non_existing_key")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_uri("uri_non_existing_key", is_list=True)

        self.assertEqual(
            self.config.get_uri("uri_non_existing_key", is_optional=True), None
        )
        self.assertEqual(
            self.config.get_uri(
                "uri_non_existing_key",
                is_optional=True,
                default=V1UriType("user2", "pass", "localhost:8080"),
            ),
            V1UriType("user2", "pass", "localhost:8080"),
        )

        self.assertEqual(
            self.config.get_uri("uri_non_existing_key", is_list=True, is_optional=True),
            None,
        )

        self.assertEqual(
            self.config.get_uri(
                "uri_non_existing_key",
                is_list=True,
                is_optional=True,
                default=[
                    V1UriType("user", "pass", "siteweb.ca"),
                    V1UriType("user2", "pass", "localhost:8080"),
                ],
            ),
            [
                V1UriType("user", "pass", "siteweb.ca"),
                V1UriType("user2", "pass", "localhost:8080"),
            ],
        )

    def test_get_auth(self):
        value = self.config.get_auth("auth_key_1")
        self.assertEqual(value, V1AuthType("user", "pass"))

        value = self.config.get_auth("auth_list_key_1", is_list=True)
        self.assertEqual(
            value, [V1AuthType("user", "pass"), V1AuthType("user2", "pass")]
        )

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_auth("auth_error_key_1")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_auth("auth_error_key_2")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_auth("auth_error_key_3")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_auth("auth_error_key_4")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_auth("auth_list_key_1")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_auth("auth_list_error_key_1", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_auth("auth_list_error_key_2", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_auth("auth_list_error_key_3", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_auth("auth_list_error_key_4", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_auth("auth_key_1", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_auth("auth_non_existing_key")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_auth("auth_non_existing_key", is_list=True)

        self.assertEqual(
            self.config.get_auth("auth_non_existing_key", is_optional=True), None
        )
        self.assertEqual(
            self.config.get_auth(
                "auth_non_existing_key",
                is_optional=True,
                default=V1AuthType("user2", "pass"),
            ),
            V1AuthType("user2", "pass"),
        )

        self.assertEqual(
            self.config.get_auth(
                "auth_non_existing_key", is_list=True, is_optional=True
            ),
            None,
        )
        self.assertEqual(
            self.config.get_auth(
                "auth_non_existing_key",
                is_list=True,
                is_optional=True,
                default=[V1AuthType("user", "pass"), V1AuthType("user2", "pass")],
            ),
            [V1AuthType("user", "pass"), V1AuthType("user2", "pass")],
        )

    def test_get_list(self):
        value = self.config.get_list("list_key_1")
        self.assertEqual(value, ["user:pass@siteweb.ca", "'pp'", "0.1", "'foo'"])

        value = self.config.get_list("list_key_2")
        self.assertEqual(value, ["user1", "user2", "user3", "user4", "user5"])

        value = self.config.get_list("list_key_3")
        self.assertEqual(value, [False])

        value = self.config.get_list("list_key_4")
        self.assertEqual(value, ["foo"])

        value = self.config.get_list("list_key_5")
        self.assertEqual(value, [])

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_list("list_error_key_1")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_list("list_error_key_2")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_list("list_error_key_3")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_list("list_error_key_4")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_list("list_non_existing_key")

        self.assertEqual(
            self.config.get_list("list_non_existing_key", is_optional=True), None
        )
        self.assertEqual(
            self.config.get_list(
                "list_non_existing_key", is_optional=True, default=["foo"]
            ),
            ["foo"],
        )

    def test_get_dict_of_dicts(self):
        value = self.config.get_dict_of_dicts("dict_dicts_key_1")
        self.assertEqual(
            value, {"data1": {"mountPath": "/data/21", "existingClaim": "data-1-pvc"}}
        )

        value = self.config.get_dict_of_dicts("dict_dicts_key_2")
        self.assertEqual(
            value,
            {
                "outputs1": {
                    "mountPath": "/output/2",
                    "existingClaim": "outputs-1-pvc",
                },
                "outputs2": {"mountPath": "/output/2", "existingClaim": "output-2-pvc"},
            },
        )

        value = self.config.get_dict_of_dicts("dict_dicts_key_3")
        self.assertEqual(value, None)

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_dict_of_dicts("dict_dicts_error_key_1")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_dict_of_dicts("dict_dicts_error_key_2")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_dict_of_dicts("dict_dicts_error_key_3")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_dict_of_dicts("dict_dicts_error_key_4")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_dict_of_dicts("dict_dicts_error_key_5")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_dict_of_dicts("dict_dicts_error_key_6")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_dict_of_dicts("dict_dicts_error_key_7")

        with self.assertRaises(PolyaxonSchemaError):
            self.config.get_dict_of_dicts("dict_dicts_non_existing_key")

        self.assertEqual(
            self.config.get_dict_of_dicts(
                "dict_dicts_non_existing_key", is_optional=True
            ),
            None,
        )
        self.assertEqual(
            self.config.get_dict_of_dicts(
                "dict_dicts_non_existing_key", is_optional=True, default={}
            ),
            {},
        )
