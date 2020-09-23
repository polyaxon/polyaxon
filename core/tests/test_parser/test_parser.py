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
import datetime

import pytest

from dateutil.tz import tzutc
from tests.utils import BaseTestCase

from polyaxon.exceptions import PolyaxonSchemaError
from polyaxon.parser import parser
from polyaxon.parser.constants import NO_VALUE_FOUND
from polyaxon.schemas.types import (
    V1ArtifactsType,
    V1AuthType,
    V1DockerfileType,
    V1GcsType,
    V1GitType,
    V1S3Type,
    V1UriType,
    V1WasbType,
)


@pytest.mark.parser_mark
class TestParser(BaseTestCase):
    def test_get_boolean(self):
        value = parser.get_boolean(key="bool_key_1", value="1")
        self.assertEqual(value, True)

        value = parser.get_boolean(key="bool_key_2", value="true")
        self.assertEqual(value, True)

        value = parser.get_boolean(key="bool_key_2", value=True)
        self.assertEqual(value, True)

        value = parser.get_boolean(key="bool_key_3", value="0")
        self.assertEqual(value, False)

        value = parser.get_boolean(key="bool_key_4", value="false")
        self.assertEqual(value, False)

        value = parser.get_boolean(key="bool_key_4", value=False)
        self.assertEqual(value, False)

        value = parser.get_boolean(
            key="bool_list_key_1",
            value=[False, "false", True, "true", "1", "0"],
            is_list=True,
        )
        self.assertEqual(value, [False, False, True, True, True, False])

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_boolean(key="bool_error_key_1", value="null")

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_boolean(key="bool_error_key_1", value=None)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_boolean(key="bool_error_key_2", value="foo")

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_boolean(key="bool_error_key_3", value=0)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_boolean(key="bool_error_key_4", value=1)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_boolean(key="bool_error_key_5", value="")

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_boolean(
                key="bool_list_key_1", value=[False, "false", True, "true", "1", "0"]
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_boolean(
                key="bool_list_error_key_2", value=[False, 1, 0], is_list=True
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_boolean(
                key="bool_list_error_key_1",
                value=[False, "false", True, "true", "1", "0", "foo"],
                is_list=True,
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_boolean(key="bool_key_1", value="1", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_boolean(key="bool_key_2", value=True, is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_boolean(key="bool_non_existing_key", value=None)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_boolean(key="bool_non_existing_key", value=NO_VALUE_FOUND)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_boolean(key="bool_non_existing_key", value=None, is_list=True)

        self.assertEqual(
            parser.get_boolean(
                key="bool_non_existing_key", value=None, is_optional=True
            ),
            None,
        )
        self.assertEqual(
            parser.get_boolean(
                key="bool_non_existing_key", value=None, is_optional=True, default=True
            ),
            True,
        )

        self.assertEqual(
            parser.get_boolean(
                key="bool_non_existing_key", value=None, is_list=True, is_optional=True
            ),
            None,
        )
        self.assertEqual(
            parser.get_boolean(
                key="bool_non_existing_key",
                value=None,
                is_list=True,
                is_optional=True,
                default=[True, False],
            ),
            [True, False],
        )

    def test_get_int(self):
        value = parser.get_int(key="int_key_1", value=123)
        self.assertEqual(value, 123)

        value = parser.get_int(key="int_key_2", value="123")
        self.assertEqual(value, 123)

        value = parser.get_int(
            key="int_list_key_1", value=["123", 124, 125, "125"], is_list=True
        )
        self.assertEqual(value, [123, 124, 125, 125])

        value = parser.get_int(
            key="int_list_key_1", value='["123", 124, 125, "125"]', is_list=True
        )
        self.assertEqual(value, [123, 124, 125, 125])

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_int(key="int_error_key_1", value="null")

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_int(key="int_error_key_1", value=None)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_int(key="int_error_key_2", value="")

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_int(key="int_error_key_3", value="foo")

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_int(key="int_list_key_1", value=["123", 124, 125, "125"])

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_int(
                key="int_list_error_key_1",
                value=["123", 124, 125, "125", None],
                is_list=True,
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_int(
                key="int_list_error_key_2",
                value=["123", 1.24, 125, "125"],
                is_list=True,
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_int(
                key="int_list_error_key_3",
                value=["123", 1.24, 125, "foo"],
                is_list=True,
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_int(key="int_key_1", value=125, is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_int(key="int_key_2", value="125", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_int(key="int_non_existing_key", value=None)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_int(key="int_non_existing_key", value=NO_VALUE_FOUND)

        self.assertEqual(
            parser.get_int(key="int_non_existing_key", value=None, is_optional=True),
            None,
        )
        self.assertEqual(
            parser.get_int(
                key="int_non_existing_key", value=None, is_optional=True, default=34
            ),
            34,
        )

        self.assertEqual(
            parser.get_int(
                key="int_non_existing_key", value=None, is_list=True, is_optional=True
            ),
            None,
        )
        self.assertEqual(
            parser.get_int(
                key="int_non_existing_key",
                value=None,
                is_list=True,
                is_optional=True,
                default=[34, 1],
            ),
            [34, 1],
        )

    def test_get_float(self):
        value = parser.get_float(key="float_key_1", value=1.23)
        self.assertEqual(value, 1.23)

        value = parser.get_float(key="float_key_2", value="1.23")
        self.assertEqual(value, 1.23)

        value = parser.get_float(key="float_key_3", value="123")
        self.assertEqual(value, 123)

        value = parser.get_float(
            key="float_list_key_1", value=[1.23, 13.3, "4.4", "555", 66.0], is_list=True
        )
        self.assertEqual(value, [1.23, 13.3, 4.4, 555.0, 66.0])

        value = parser.get_float(
            key="float_list_key_1",
            value='[1.23, 13.3, "4.4", "555", 66.0]',
            is_list=True,
        )
        self.assertEqual(value, [1.23, 13.3, 4.4, 555.0, 66.0])

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_float(key="float_error_key_1", value=None)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_float(key="float_error_key_1", value="null")

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_float(key="float_error_key_2", value="")

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_float(key="float_error_key_3", value="foo")

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_float(key="float_error_key_4", value=123)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_float(
                key="float_list_key_1", value=[1.23, 13.3, "4.4", "555", 66.0]
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_float(key="float_list_error_key_1", value=None, is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_float(key="float_list_error_key_2", value="", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_float(key="float_list_error_key_3", value="foo", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_float(key="float_key_1", value=213, is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_float(key="float_key_2", value=[1.23, 13.3, 66], is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_float(key="float_non_existing_key", value=NO_VALUE_FOUND)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_float(key="float_non_existing_key", value=[1.23, 13.3, "foo"])

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_float(
                key="float_non_existing_key", value=[1.23, 13.3, None], is_list=True
            )

        self.assertEqual(
            parser.get_float(
                key="float_non_existing_key", value=None, is_optional=True
            ),
            None,
        )
        self.assertEqual(
            parser.get_float(
                key="float_non_existing_key", value=None, is_optional=True, default=3.4
            ),
            3.4,
        )

        self.assertEqual(
            parser.get_float(
                key="float_non_existing_key",
                value="null",
                is_list=True,
                is_optional=True,
            ),
            None,
        )
        self.assertEqual(
            parser.get_float(
                key="float_non_existing_key",
                value=None,
                is_list=True,
                is_optional=True,
                default=[3.4, 1.2],
            ),
            [3.4, 1.2],
        )

    def test_get_string(self):
        value = parser.get_string(key="string_key_1", value="123")
        self.assertEqual(value, "123")

        value = parser.get_string(key="string_key_2", value="1.23")
        self.assertEqual(value, "1.23")

        value = parser.get_string(key="string_key_3", value="foo")
        self.assertEqual(value, "foo")

        value = parser.get_string(key="string_key_4", value="")
        self.assertEqual(value, "")

        value = parser.get_string(
            key="string_list_key_1", value=["123", "1.23", "foo", ""], is_list=True
        )
        self.assertEqual(value, ["123", "1.23", "foo", ""])

        value = parser.get_string(
            key="string_list_key_1", value='["123", "1.23", "foo", ""]', is_list=True
        )
        self.assertEqual(value, ["123", "1.23", "foo", ""])

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_string(key="string_error_key_1", value=None)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_string(key="string_error_key_2", value=123)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_string(key="string_error_key_3", value=1.23)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_string(key="string_error_key_4", value=True)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_string(key="string_list_key_1", value=["123", "1.23", "foo", ""])

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_string(
                key="string_list_error_key_1", value=["123", 123], is_list=True
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_string(
                key="string_list_error_key_2", value=["123", 12.3], is_list=True
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_string(
                key="string_list_error_key_3", value=["123", None], is_list=True
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_string(
                key="string_list_error_key_4", value=["123", False], is_list=True
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_string(key="string_key_3", value="foo", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_string(key="string_key_4", value="", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_string(key="string_non_existing_key", value=None)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_string(key="string_non_existing_key", value=NO_VALUE_FOUND)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_string(key="string_non_existing_key", value=None, is_list=True)

        self.assertEqual(
            parser.get_string(
                key="string_non_existing_key", value=None, is_optional=True
            ),
            None,
        )
        self.assertEqual(
            parser.get_string(
                key="string_non_existing_key",
                value=None,
                is_optional=True,
                default="foo",
            ),
            "foo",
        )

        self.assertEqual(
            parser.get_string(
                key="string_non_existing_key",
                value=None,
                is_list=True,
                is_optional=True,
            ),
            None,
        )
        self.assertEqual(
            parser.get_string(
                key="string_non_existing_key",
                value=None,
                is_list=True,
                is_optional=True,
                default=["foo", "bar"],
            ),
            ["foo", "bar"],
        )

    def test_get_dict(self):
        value = parser.get_dict(
            key="dict_key_1",
            value={"key1": "foo", "key2": 2, "key3": False, "key4": "1"},
        )
        self.assertEqual(value, {"key1": "foo", "key2": 2, "key3": False, "key4": "1"})

        value = parser.get_dict(
            key="dict_key_1",
            value='{"key1": "foo", "key2": 2, "key3": false, "key4": "1"}',
        )
        self.assertEqual(value, {"key1": "foo", "key2": 2, "key3": False, "key4": "1"})

        value = parser.get_dict(
            key="dict_key_1",
            value='{"key1": "foo", "key2": 2, "key3": false, "key4": "1"}',
        )
        self.assertEqual(value, {"key1": "foo", "key2": 2, "key3": False, "key4": "1"})

        value = parser.get_dict(
            key="dict_list_key_1",
            value=[
                {"key1": "foo", "key2": 2, "key3": False, "key4": "1"},
                {"key3": True, "key4": "2"},
                {"key1": False, "key2": "3"},
            ],
            is_list=True,
        )
        self.assertEqual(
            value,
            [
                {"key1": "foo", "key2": 2, "key3": False, "key4": "1"},
                {"key3": True, "key4": "2"},
                {"key1": False, "key2": "3"},
            ],
        )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dict(key="dict_error_key_1", value="foo")

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dict(key="dict_error_key_2", value=1)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dict(key="dict_error_key_3", value=False)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dict(key="dict_error_key_4", value=["1", "foo"])

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dict(key="dict_list_key_1", value=["123", {"key3": True}])

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dict(
                key="dict_list_error_key_1", value=["123", {"key3": True}], is_list=True
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dict(
                key="dict_list_error_key_2", value=[{"key3": True}, 12.3], is_list=True
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dict(
                key="dict_list_error_key_3", value=[{"key3": True}, None], is_list=True
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dict(
                key="dict_list_error_key_4",
                value=[{"key3": True}, "123", False],
                is_list=True,
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dict(
                key="dict_key_1",
                value={"key1": "foo", "key2": 2, "key3": False, "key4": "1"},
                is_list=True,
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dict(key="dict_non_existing_key", value=None)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dict(key="dict_non_existing_key", value=NO_VALUE_FOUND)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dict(key="dict_non_existing_key", value=None, is_list=True)

        self.assertEqual(
            parser.get_dict(key="dict_non_existing_key", value=None, is_optional=True),
            None,
        )
        self.assertEqual(
            parser.get_dict(
                key="dict_non_existing_key",
                value=None,
                is_optional=True,
                default={"foo": "bar"},
            ),
            {"foo": "bar"},
        )

        self.assertEqual(
            parser.get_dict(
                key="dict_non_existing_key", value=None, is_list=True, is_optional=True
            ),
            None,
        )
        self.assertEqual(
            parser.get_dict(
                key="dict_non_existing_key",
                value=None,
                is_list=True,
                is_optional=True,
                default=[{"foo": "bar"}, {"foo": "boo"}],
            ),
            [{"foo": "bar"}, {"foo": "boo"}],
        )

    def test_get_uri(self):
        value = parser.get_uri(key="uri_key_1", value="user:pass@siteweb.ca")
        self.assertEqual(value, V1UriType("user", "pass", "siteweb.ca"))

        value = parser.get_uri(key="uri_key_2", value="user2:pass@localhost:8080")
        self.assertEqual(value, V1UriType("user2", "pass", "localhost:8080"))

        value = parser.get_uri(key="uri_key_3", value="user2:pass@https://quay.io")
        self.assertEqual(value, V1UriType("user2", "pass", "https://quay.io"))

        value = parser.get_uri(
            key="uri_list_key_1",
            value=[
                "user:pass@siteweb.ca",
                "user2:pass@localhost:8080",
                "user2:pass@https://quay.io",
            ],
            is_list=True,
        )
        self.assertEqual(
            value,
            [
                V1UriType("user", "pass", "siteweb.ca"),
                V1UriType("user2", "pass", "localhost:8080"),
                V1UriType("user2", "pass", "https://quay.io"),
            ],
        )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_uri(key="uri_error_key_1", value="foo")

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_uri(key="uri_error_key_2", value=1)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_uri(key="uri_error_key_3", value=False)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_uri(key="uri_error_key_4", value=["1", "foo"])

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_uri(
                key="uri_list_key_1",
                value=[
                    "user:pass@siteweb.ca",
                    "user2:pass@localhost:8080",
                    "user2:pass@https://quay.io",
                ],
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_uri(
                key="uri_list_error_key_1",
                value=["123", "user:pass@siteweb.ca"],
                is_list=True,
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_uri(
                key="uri_list_error_key_2",
                value=["user:pass@siteweb.ca", 12.3],
                is_list=True,
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_uri(
                key="uri_list_error_key_3",
                value=["user:pass@siteweb.ca", None],
                is_list=True,
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_uri(
                key="uri_list_error_key_4",
                value=["user:pass@siteweb.ca", "123", False],
                is_list=True,
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_uri(key="uri_key_1", value="user:pass@siteweb.ca", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_uri(key="uri_non_existing_key", value=None)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_uri(key="uri_non_existing_key", value=NO_VALUE_FOUND)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_uri(key="uri_non_existing_key", value=None, is_list=True)

        self.assertEqual(
            parser.get_uri(key="uri_non_existing_key", value=None, is_optional=True),
            None,
        )
        self.assertEqual(
            parser.get_uri(
                key="uri_non_existing_key",
                value=None,
                is_optional=True,
                default=V1UriType("user2", "pass", "localhost:8080"),
            ),
            V1UriType("user2", "pass", "localhost:8080"),
        )

        self.assertEqual(
            parser.get_uri(
                key="uri_non_existing_key", value=None, is_list=True, is_optional=True
            ),
            None,
        )
        self.assertEqual(
            parser.get_uri(
                key="uri_non_existing_key",
                value=None,
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
        value = parser.get_auth(
            key="auth_key_1", value={"user": "user", "password": "pass"}
        )
        self.assertEqual(value, V1AuthType("user", "pass"))

        value = parser.get_auth(key="auth_key_1", value=V1AuthType("user", "pass"))
        self.assertEqual(value, V1AuthType("user", "pass"))

        value = parser.get_auth(key="auth_key_1", value="user:pass")
        self.assertEqual(value, V1AuthType("user", "pass"))

        value = parser.get_auth(
            key="auth_list_key_1", value=["user:pass", "user2:pass"], is_list=True
        )
        self.assertEqual(
            value, [V1AuthType("user", "pass"), V1AuthType("user2", "pass")]
        )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_auth(key="auth_error_key_1", value="foo")

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_auth(key="auth_error_key_2", value=1)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_auth(key="auth_error_key_3", value=False)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_auth(key="auth_error_key_4", value=["1", "foo"])

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_auth(key="auth_list_key_1", value=["user:pass", "user2:pass"])

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_auth(
                key="auth_list_error_key_1", value=["123", "user:pass"], is_list=True
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_auth(
                key="auth_list_error_key_2", value=["user:pass", 12.3], is_list=True
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_auth(
                key="auth_list_error_key_3", value=["user:pass", None], is_list=True
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_auth(
                key="auth_list_error_key_4",
                value=["user:pass", "123", False],
                is_list=True,
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_auth(key="auth_key_1", value="user:pass", is_list=True)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_auth(key="auth_non_existing_key", value=None)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_auth(key="auth_non_existing_key", value=NO_VALUE_FOUND)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_auth(key="auth_non_existing_key", value=None, is_list=True)

        self.assertEqual(
            parser.get_auth(key="auth_non_existing_key", value=None, is_optional=True),
            None,
        )
        self.assertEqual(
            parser.get_auth(
                key="auth_non_existing_key",
                value=None,
                is_optional=True,
                default=V1AuthType("user2", "pass"),
            ),
            V1AuthType("user2", "pass"),
        )

        self.assertEqual(
            parser.get_auth(
                key="auth_non_existing_key", value=None, is_list=True, is_optional=True
            ),
            None,
        )
        self.assertEqual(
            parser.get_auth(
                key="auth_non_existing_key",
                value=None,
                is_list=True,
                is_optional=True,
                default=[V1AuthType("user", "pass"), V1AuthType("user2", "pass")],
            ),
            [V1AuthType("user", "pass"), V1AuthType("user2", "pass")],
        )

    def test_get_list(self):
        value = parser.get_list(
            key="list_key_1", value="user:pass@siteweb.ca, 'pp', 0.1, 'foo'"
        )
        self.assertEqual(value, ["user:pass@siteweb.ca", "'pp'", "0.1", "'foo'"])

        value = parser.get_list(
            key="list_key_2", value="user1,user2 , user3,     user4    , user5"
        )
        self.assertEqual(value, ["user1", "user2", "user3", "user4", "user5"])

        value = parser.get_list(key="list_key_3", value=[False])
        self.assertEqual(value, [False])

        value = parser.get_list(key="list_key_3", value=["false"])
        self.assertEqual(value, ["false"])

        value = parser.get_list(key="list_key_4", value="foo")
        self.assertEqual(value, ["foo"])

        value = parser.get_list(key="list_key_5", value="")
        self.assertEqual(value, [])

        value = parser.get_list(key="list_error_key_3", value="null")
        self.assertEqual(value, ["null"])

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_list(key="list_error_key_1", value=True)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_list(key="list_error_key_2", value={"key": "value"})

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_list(key="list_error_key_4", value=123)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_list(key="list_non_existing_key", value=None)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_list(key="list_non_existing_key", value=NO_VALUE_FOUND)

        self.assertEqual(
            parser.get_list(key="list_non_existing_key", value=None, is_optional=True),
            None,
        )
        self.assertEqual(
            parser.get_list(
                key="list_non_existing_key",
                value=None,
                is_optional=True,
                default=["foo"],
            ),
            ["foo"],
        )

    def test_get_dict_of_dicts(self):
        value = parser.get_dict_of_dicts(
            key="dict_dicts_key_1",
            value={"data1": {"mountPath": "/data/21", "existingClaim": "data-1-pvc"}},
        )
        self.assertEqual(
            value, {"data1": {"mountPath": "/data/21", "existingClaim": "data-1-pvc"}}
        )

        value = parser.get_dict_of_dicts(
            key="dict_dicts_key_1",
            value='{"data1": {"mountPath": "/data/21", "existingClaim": "data-1-pvc"}}',
        )
        self.assertEqual(
            value, {"data1": {"mountPath": "/data/21", "existingClaim": "data-1-pvc"}}
        )

        value = parser.get_dict_of_dicts(
            key="dict_dicts_key_2",
            value={
                "outputs1": {
                    "mountPath": "/output/2",
                    "existingClaim": "outputs-1-pvc",
                },
                "outputs2": {"mountPath": "/output/2", "existingClaim": "output-2-pvc"},
            },
        )
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

        value = parser.get_dict_of_dicts(key="dict_dicts_key_3", value={})
        self.assertEqual(value, None)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dict_of_dicts(key="dict_dicts_error_key_1", value=True)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dict_of_dicts(
                key="dict_dicts_error_key_2", value={"key": "value"}
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dict_of_dicts(key="dict_dicts_error_key_3", value="null")

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dict_of_dicts(key="dict_dicts_error_key_4", value=123)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dict_of_dicts(key="dict_dicts_error_key_5", value="foo")

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dict_of_dicts(key="dict_dicts_error_key_6", value="")

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dict_of_dicts(
                key="dict_dicts_error_key_7",
                value={"mountPath": "/data/2", "existingClaim": "data-2-pvc"},
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dict_of_dicts(key="dict_dicts_non_existing_key", value=None)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dict_of_dicts(
                key="dict_dicts_non_existing_key", value=NO_VALUE_FOUND
            )

        self.assertEqual(
            parser.get_dict_of_dicts(
                key="dict_dicts_non_existing_key", value=None, is_optional=True
            ),
            None,
        )
        self.assertEqual(
            parser.get_dict_of_dicts(
                key="dict_dicts_non_existing_key",
                value=None,
                is_optional=True,
                default={},
            ),
            {},
        )

    def test_get_wasbs_path(self):
        # Correct url
        wasbs_path = "wasbs://container@user.blob.core.windows.net/path"
        expected = V1WasbType("container", "user", "path")
        parsed_url = parser.parse_wasbs_path(wasbs_path)
        assert parsed_url == expected
        parsed_url = parser.get_wasbs_path(key="wasb_key", value=wasbs_path)
        assert parsed_url == expected

        wasbs_path = "wasbs://container@user.blob.core.windows.net/"
        expected = V1WasbType("container", "user", "")
        parsed_url = parser.parse_wasbs_path(wasbs_path)
        assert parsed_url == expected
        parsed_url = parser.get_wasbs_path(key="wasb_key", value=wasbs_path)
        assert parsed_url == expected

        wasbs_path = "wasbs://container@user.blob.core.windows.net"
        expected = V1WasbType("container", "user", "")
        parsed_url = parser.parse_wasbs_path(wasbs_path)
        assert parsed_url == expected
        parsed_url = parser.get_wasbs_path(key="wasb_key", value=wasbs_path)
        assert parsed_url == expected

        wasbs_path = "wasbs://container@user.blob.core.windows.net/path/to/file"
        expected = V1WasbType("container", "user", "path/to/file")
        parsed_url = parser.parse_wasbs_path(wasbs_path)
        assert parsed_url == expected
        parsed_url = parser.get_wasbs_path(key="wasb_key", value=wasbs_path)
        assert parsed_url == expected

        # Wrong url
        wasbs_path = "wasbs://container@user.foo.bar.windows.net/path/to/file"
        with self.assertRaises(PolyaxonSchemaError):
            parser.parse_wasbs_path(wasbs_path)
        with self.assertRaises(PolyaxonSchemaError):
            parser.get_wasbs_path(key="wasb_key", value=wasbs_path)

        wasbs_path = "wasbs://container@user.blob.core.foo.net/path/to/file"
        with self.assertRaises(PolyaxonSchemaError):
            parser.parse_wasbs_path(wasbs_path)
        with self.assertRaises(PolyaxonSchemaError):
            parser.get_wasbs_path(key="wasb_key", value=wasbs_path)

        wasbs_path = "wasbs://container@user.blob.windows.net/path/to/file"
        with self.assertRaises(PolyaxonSchemaError):
            parser.parse_wasbs_path(wasbs_path)
        with self.assertRaises(PolyaxonSchemaError):
            parser.get_wasbs_path(key="wasb_key", value=wasbs_path)

    def test_parse_gcs_path(self):
        # Correct url
        gcs_path = "gs://bucket/path/to/blob"
        expected = V1GcsType("bucket", "path/to/blob")
        parsed_url = parser.parse_gcs_path(gcs_path)
        assert parsed_url == expected
        parsed_url = parser.get_gcs_path(key="gcs_key", value=gcs_path)
        assert parsed_url == expected

        # Wrong url
        gcs_path = "gs:/bucket/path/to/blob"
        with self.assertRaises(PolyaxonSchemaError):
            parser.parse_gcs_path(gcs_path)
        with self.assertRaises(PolyaxonSchemaError):
            parser.get_gcs_path(key="gcs_key", value=gcs_path)

        # Trailing slash
        gcs_path = "gs://bucket/path/to/blob/"
        expected = V1GcsType("bucket", "path/to/blob/")
        assert parser.parse_gcs_path(gcs_path) == expected
        parsed_url = parser.get_gcs_path(key="gcs_key", value=gcs_path)
        assert parsed_url == expected

        # Bucket only
        gcs_path = "gs://bucket/"
        expected = V1GcsType("bucket", "")
        assert parser.parse_gcs_path(gcs_path) == expected
        parsed_url = parser.get_gcs_path(key="gcs_key", value=gcs_path)
        assert parsed_url == expected

    def test_parse_s3_path(self):
        s3_path = "s3://test/this/is/bad/key.txt"
        expected = V1S3Type("test", "this/is/bad/key.txt")
        parsed_url = parser.parse_s3_path(s3_path)
        assert parsed_url == expected
        parsed_url = parser.get_s3_path(key="s3_key", value=s3_path)
        assert parsed_url == expected

    def test_parse_date(self):
        value = "2010-12-12"
        parsed_url = parser.get_date(key="date_key", value=value)
        assert parsed_url == datetime.date(2010, 12, 12)

        value = datetime.date(2010, 12, 12)
        parsed_url = parser.get_date(key="date_key", value=value)
        assert parsed_url == value

        value = "2010-12-12-12"
        with self.assertRaises(PolyaxonSchemaError):
            parser.get_date(key="date_key", value=value)

    def test_parse_datetime(self):
        value = "2010-12-12 10:10"
        parsed_url = parser.get_datetime(key="date_key", value=value)
        assert parsed_url == datetime.datetime(2010, 12, 12, 10, 10)

        value = "2010-12-12 01:00"
        parsed_url = parser.get_datetime(key="date_key", value=value)
        assert parsed_url == datetime.datetime(2010, 12, 12, 1, 0)

        value = "2010-12-12 01:53:12"
        parsed_url = parser.get_datetime(key="date_key", value=value)
        assert parsed_url == datetime.datetime(2010, 12, 12, 1, 53, 12)

        value = "2014-12-22T03:12:58.019077+00:00"
        parsed_url = parser.get_datetime(key="date_key", value=value)
        assert parsed_url == datetime.datetime(
            2014, 12, 22, 3, 12, 58, 19077, tzinfo=tzutc()
        )

        value = datetime.datetime(2010, 12, 12, 0, 0, 0)
        parsed_url = parser.get_date(key="date_key", value=value)
        assert parsed_url == value

        value = datetime.datetime(2010, 12, 12, 0, 0, 0, tzinfo=tzutc())
        parsed_url = parser.get_date(key="date_key", value=value)
        assert parsed_url == value

        # Dates are not validate by datetime
        value = "2010-12-12"
        with self.assertRaises(PolyaxonSchemaError):
            parser.get_datetime(key="date_key", value=value)

    def test_get_dockerfile_init(self):
        value = parser.get_dockerfile_init(
            key="dict_key_1", value={"image": "foo", "env": {"key1": 2, "key2": 21}}
        )
        self.assertEqual(
            value, V1DockerfileType(image="foo", env={"key1": 2, "key2": 21})
        )

        value = parser.get_dockerfile_init(
            key="dict_key_1", value='{"image": "foo", "env": {"key1": 2, "key2": 21}}'
        )
        self.assertEqual(
            value, V1DockerfileType(image="foo", env={"key1": 2, "key2": 21})
        )

        value = parser.get_dockerfile_init(
            key="dict_key_1", value='{"image": "foo", "run": ["exec1", "exec2"]}'
        )
        self.assertEqual(value, V1DockerfileType(image="foo", run=["exec1", "exec2"]))

        value = parser.get_dockerfile_init(
            key="dict_list_key_1",
            value=[
                {"image": "foo", "env": {"key1": 2, "key2": 21}},
                {"image": "foo2", "copy": ["exec1", "exec2"]},
                {"image": "foo3", "run": ["exec1", "exec2"]},
            ],
            is_list=True,
        )
        self.assertEqual(
            value,
            [
                V1DockerfileType(image="foo", env={"key1": 2, "key2": 21}),
                V1DockerfileType(image="foo2", copy=["exec1", "exec2"]),
                V1DockerfileType(image="foo3", run=["exec1", "exec2"]),
            ],
        )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dockerfile_init(key="dict_error_key_1", value=None)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dockerfile_init(key="dict_error_key_1", value="foo")

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dockerfile_init(key="dict_error_key_2", value=1)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dockerfile_init(key="dict_error_key_3", value=False)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dockerfile_init(key="dict_error_key_4", value=["1", "foo"])

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dockerfile_init(
                key="dict_list_key_1", value=["123", {"key3": True}]
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dockerfile_init(
                key="dict_list_error_key_1", value=["123", {"key3": True}], is_list=True
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dockerfile_init(
                key="dict_list_error_key_2", value=[{"key3": True}, 12.3], is_list=True
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dockerfile_init(
                key="dict_list_error_key_3", value=[{"key3": True}, None], is_list=True
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dockerfile_init(
                key="dict_list_error_key_4",
                value=[{"key3": True}, "123", False],
                is_list=True,
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dockerfile_init(
                key="dict_key_1",
                value={"key1": "foo", "key2": 2, "key3": False, "key4": "1"},
                is_list=True,
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dockerfile_init(key="dict_non_existing_key", value=None)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dockerfile_init(
                key="dict_non_existing_key", value=NO_VALUE_FOUND
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_dockerfile_init(
                key="dict_non_existing_key", value=None, is_list=True
            )

        self.assertEqual(
            parser.get_dockerfile_init(
                key="dict_non_existing_key", value=None, is_optional=True
            ),
            None,
        )

    def test_get_git_init(self):
        value = parser.get_git_init(key="dict_key_1", value={"revision": "foo"})
        self.assertEqual(value, V1GitType(revision="foo"))

        value = parser.get_git_init(key="dict_key_1", value={"revision": "foo"},)
        self.assertEqual(value, V1GitType(revision="foo"))

        value = parser.get_git_init(
            key="dict_key_1", value={"url": "https://github.com", "revision": "foo"}
        )
        self.assertEqual(value, V1GitType(revision="foo", url="https://github.com"))

        value = parser.get_git_init(
            key="dict_key_1", value='{"revision": "foo", "url": "https://github.com"}'
        )
        self.assertEqual(value, V1GitType(revision="foo", url="https://github.com"))

        value = parser.get_git_init(key="dict_key_1", value='{"revision": "foo"}')
        self.assertEqual(value, V1GitType(revision="foo"))

        value = parser.get_git_init(
            key="dict_list_key_1",
            value=[
                {"revision": "foo"},
                {"url": "https://github.com", "revision": "foo"},
                {"url": "https://github.com"},
            ],
            is_list=True,
        )
        self.assertEqual(
            value,
            [
                V1GitType(revision="foo"),
                V1GitType(revision="foo", url="https://github.com"),
                V1GitType(url="https://github.com"),
            ],
        )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_git_init(
                key="dict_error_key_1",
                value=dict(revision="foo", connection="foo", init=True),
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_git_init(
                key="dict_error_key_1", value=dict(revision="foo", init=True)
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_git_init(
                key="dict_error_key_1", value=dict(revision="foo", connection="foo")
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_git_init(key="dict_error_key_1", value="foo")

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_git_init(key="dict_error_key_2", value=1)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_git_init(key="dict_error_key_3", value=False)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_git_init(key="dict_error_key_4", value=["1", "foo"])

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_git_init(key="dict_list_key_1", value=["123", {"key3": True}])

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_git_init(
                key="dict_list_error_key_1", value=["123", {"key3": True}], is_list=True
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_git_init(
                key="dict_list_error_key_2", value=[{"key3": True}, 12.3], is_list=True
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_git_init(
                key="dict_list_error_key_3", value=[{"key3": True}, None], is_list=True
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_git_init(
                key="dict_list_error_key_4",
                value=[{"key3": True}, "123", False],
                is_list=True,
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_git_init(
                key="dict_key_1",
                value={"key1": "foo", "key2": 2, "key3": False, "key4": "1"},
                is_list=True,
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_git_init(key="dict_non_existing_key", value=None)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_git_init(key="dict_non_existing_key", value=NO_VALUE_FOUND)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_git_init(key="dict_non_existing_key", value=None, is_list=True)

        self.assertEqual(
            parser.get_git_init(
                key="dict_non_existing_key", value=None, is_optional=True
            ),
            None,
        )

    def test_get_image_init(self):
        value = parser.get_image_init(key="dict_key_1", value="foo")
        self.assertEqual(value, "foo")

        value = parser.get_image_init(key="dict_key_1", value={"name": "foo"})
        self.assertEqual(value, "foo")

        value = parser.get_image_init(key="dict_key_1", value="foo:bar")
        self.assertEqual(value, "foo:bar")

        value = parser.get_image_init(
            key="dict_key_1", value={"name": "foo:bar", "connection": "foo"}
        )
        self.assertEqual(value, "foo:bar")

        value = parser.get_image_init(
            key="dict_key_1", value="https://registry.com/foo:bar"
        )
        self.assertEqual(value, "https://registry.com/foo:bar")

        value = parser.get_image_init(
            key="dict_key_1", value='{"name": "https://registry.com/foo:bar"}'
        )
        self.assertEqual(value, "https://registry.com/foo:bar")

        value = parser.get_image_init(
            key="dict_list_key_1",
            value=[
                {"name": "https://registry.com/foo:bar"},
                {"name": "test", "connection": "registry"},
                "foo:bar",
            ],
            is_list=True,
        )
        self.assertEqual(
            value, ["https://registry.com/foo:bar", "test", "foo:bar",],
        )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_image_init(key="dict_error_key_2", value=1)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_image_init(key="dict_error_key_3", value=False)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_image_init(key="dict_error_key_4", value=["1", "foo"])

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_image_init(key="dict_list_key_1", value=["123", {"key3": True}])

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_image_init(
                key="dict_list_error_key_1", value=["123", {"key3": True}], is_list=True
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_image_init(
                key="dict_list_error_key_2", value=[{"key3": True}, 12.3], is_list=True
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_image_init(
                key="dict_list_error_key_3", value=[{"key3": True}, None], is_list=True
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_image_init(
                key="dict_list_error_key_4",
                value=[{"key3": True}, "123", False],
                is_list=True,
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_image_init(
                key="dict_key_1",
                value={"key1": "foo", "key2": 2, "key3": False, "key4": "1"},
                is_list=True,
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_image_init(key="dict_non_existing_key", value=None)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_image_init(key="dict_non_existing_key", value=NO_VALUE_FOUND)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_image_init(key="dict_non_existing_key", value=None, is_list=True)

        self.assertEqual(
            parser.get_image_init(
                key="dict_non_existing_key", value=None, is_optional=True
            ),
            None,
        )

    def test_get_artifacts_init(self):
        value = parser.get_artifacts_init(
            key="dict_key_1", value={"files": ["foo", "bar"]}
        )
        self.assertEqual(value, V1ArtifactsType(files=["foo", "bar"]))

        value = parser.get_artifacts_init(
            key="dict_key_1", value='{"dirs": ["foo", "bar"]}'
        )
        self.assertEqual(value, V1ArtifactsType(dirs=["foo", "bar"]))

        value = parser.get_artifacts_init(
            key="dict_list_key_1",
            value=[
                {"dirs": ["foo", "bar"], "files": ["foo", "bar"]},
                {"files": ["foo", "bar"]},
            ],
            is_list=True,
        )
        self.assertEqual(
            value,
            [
                V1ArtifactsType(dirs=["foo", "bar"], files=["foo", "bar"]),
                V1ArtifactsType(files=["foo", "bar"]),
            ],
        )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_artifacts_init(
                key="dict_key_1", value={"connection": "foo", "init": True}
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_artifacts_init(
                key="dict_key_1", value={"init": True, "dirs": ["foo", "bar"]}
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_artifacts_init(
                key="dict_key_1", value={"connection": "foo", "files": ["foo", "bar"]}
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_artifacts_init(
                key="dict_error_key_1", value={"paths": ["foo", "bar"]}
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_artifacts_init(key="dict_error_key_1", value="foo")

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_artifacts_init(key="dict_error_key_2", value=1)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_artifacts_init(key="dict_error_key_3", value=False)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_artifacts_init(key="dict_error_key_4", value=["1", "foo"])

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_artifacts_init(
                key="dict_list_key_1", value=["123", {"key3": True}]
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_artifacts_init(
                key="dict_list_error_key_1", value=["123", {"key3": True}], is_list=True
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_artifacts_init(
                key="dict_list_error_key_2", value=[{"key3": True}, 12.3], is_list=True
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_artifacts_init(
                key="dict_list_error_key_3", value=[{"key3": True}, None], is_list=True
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_artifacts_init(
                key="dict_list_error_key_4",
                value=[{"key3": True}, "123", False],
                is_list=True,
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_artifacts_init(
                key="dict_key_1",
                value={"key1": "foo", "key2": 2, "key3": False, "key4": "1"},
                is_list=True,
            )

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_artifacts_init(key="dict_non_existing_key", value=None)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_artifacts_init(key="dict_non_existing_key", value=NO_VALUE_FOUND)

        with self.assertRaises(PolyaxonSchemaError):
            parser.get_artifacts_init(
                key="dict_non_existing_key", value=None, is_list=True
            )

        self.assertEqual(
            parser.get_artifacts_init(
                key="dict_non_existing_key", value=None, is_optional=True
            ),
            None,
        )
