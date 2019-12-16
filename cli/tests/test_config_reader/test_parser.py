from unittest import TestCase

from rhea import rhea_parser
from rhea.constants import NO_VALUE_FOUND
from rhea.exceptions import RheaError
from rhea.specs import AuthSpec, GCSSpec, S3Spec, UriSpec, WasbsSpec


class TestRheaParser(TestCase):

    def test_get_boolean(self):
        value = rhea_parser.get_boolean(key='bool_key_1', value="1")
        self.assertEqual(value, True)

        value = rhea_parser.get_boolean(key='bool_key_2', value="true")
        self.assertEqual(value, True)

        value = rhea_parser.get_boolean(key='bool_key_2', value=True)
        self.assertEqual(value, True)

        value = rhea_parser.get_boolean(key='bool_key_3', value="0")
        self.assertEqual(value, False)

        value = rhea_parser.get_boolean(key='bool_key_4', value="false")
        self.assertEqual(value, False)

        value = rhea_parser.get_boolean(key='bool_key_4', value=False)
        self.assertEqual(value, False)

        value = rhea_parser.get_boolean(
            key='bool_list_key_1',
            value=[False, "false", True, "true", "1", "0"],
            is_list=True)
        self.assertEqual(value, [False, False, True, True, True, False])

        with self.assertRaises(RheaError):
            rhea_parser.get_boolean(key='bool_error_key_1', value="null")

        with self.assertRaises(RheaError):
            rhea_parser.get_boolean(key='bool_error_key_1', value=None)

        with self.assertRaises(RheaError):
            rhea_parser.get_boolean(key='bool_error_key_2', value="foo")

        with self.assertRaises(RheaError):
            rhea_parser.get_boolean(key='bool_error_key_3', value=0)

        with self.assertRaises(RheaError):
            rhea_parser.get_boolean(key='bool_error_key_4', value=1)

        with self.assertRaises(RheaError):
            rhea_parser.get_boolean(key='bool_error_key_5', value="")

        with self.assertRaises(RheaError):
            rhea_parser.get_boolean(key='bool_list_key_1',
                                    value=[False, "false", True, "true", "1", "0"])

        with self.assertRaises(RheaError):
            rhea_parser.get_boolean(key='bool_list_error_key_2',
                                    value=[False, 1, 0],
                                    is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_boolean(key='bool_list_error_key_1',
                                    value=[False, "false", True, "true", "1", "0", "foo"],
                                    is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_boolean(key='bool_key_1',
                                    value="1",
                                    is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_boolean(key='bool_key_2',
                                    value=True,
                                    is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_boolean(key='bool_non_existing_key',
                                    value=None)

        with self.assertRaises(RheaError):
            rhea_parser.get_boolean(key='bool_non_existing_key',
                                    value=NO_VALUE_FOUND)

        with self.assertRaises(RheaError):
            rhea_parser.get_boolean(key='bool_non_existing_key',
                                    value=None,
                                    is_list=True)

        self.assertEqual(rhea_parser.get_boolean(
            key='bool_non_existing_key',
            value=None,
            is_optional=True), None)
        self.assertEqual(rhea_parser.get_boolean(
            key='bool_non_existing_key',
            value=None,
            is_optional=True,
            default=True), True)

        self.assertEqual(rhea_parser.get_boolean(
            key='bool_non_existing_key',
            value=None,
            is_list=True,
            is_optional=True), None)
        self.assertEqual(rhea_parser.get_boolean(
            key='bool_non_existing_key',
            value=None,
            is_list=True,
            is_optional=True,
            default=[True, False]),
            [True, False])

    def test_get_int(self):
        value = rhea_parser.get_int(key='int_key_1', value=123)
        self.assertEqual(value, 123)

        value = rhea_parser.get_int(key='int_key_2', value="123")
        self.assertEqual(value, 123)

        value = rhea_parser.get_int(key='int_list_key_1',
                                    value=["123", 124, 125, "125"],
                                    is_list=True)
        self.assertEqual(value, [123, 124, 125, 125])

        value = rhea_parser.get_int(key='int_list_key_1',
                                    value='["123", 124, 125, "125"]',
                                    is_list=True)
        self.assertEqual(value, [123, 124, 125, 125])

        with self.assertRaises(RheaError):
            rhea_parser.get_int(key='int_error_key_1', value='null')

        with self.assertRaises(RheaError):
            rhea_parser.get_int(key='int_error_key_1', value=None)

        with self.assertRaises(RheaError):
            rhea_parser.get_int(key='int_error_key_2', value='')

        with self.assertRaises(RheaError):
            rhea_parser.get_int(key='int_error_key_3', value='foo')

        with self.assertRaises(RheaError):
            rhea_parser.get_int(key='int_list_key_1', value=["123", 124, 125, "125"])

        with self.assertRaises(RheaError):
            rhea_parser.get_int(key='int_list_error_key_1',
                                value=["123", 124, 125, "125", None],
                                is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_int(key='int_list_error_key_2',
                                value=["123", 1.24, 125, "125"],
                                is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_int(key='int_list_error_key_3',
                                value=["123", 1.24, 125, "foo"],
                                is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_int(key='int_key_1', value=125, is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_int(key='int_key_2', value="125", is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_int(key='int_non_existing_key', value=None)

        with self.assertRaises(RheaError):
            rhea_parser.get_int(key='int_non_existing_key', value=NO_VALUE_FOUND)

        self.assertEqual(rhea_parser.get_int(key='int_non_existing_key',
                                             value=None,
                                             is_optional=True), None)
        self.assertEqual(rhea_parser.get_int(key='int_non_existing_key',
                                             value=None,
                                             is_optional=True,
                                             default=34), 34)

        self.assertEqual(rhea_parser.get_int(key='int_non_existing_key',
                                             value=None,
                                             is_list=True,
                                             is_optional=True), None)
        self.assertEqual(rhea_parser.get_int(key='int_non_existing_key',
                                             value=None,
                                             is_list=True,
                                             is_optional=True,
                                             default=[34, 1]), [34, 1])

    def test_get_float(self):
        value = rhea_parser.get_float(key='float_key_1', value=1.23)
        self.assertEqual(value, 1.23)

        value = rhea_parser.get_float(key='float_key_2', value="1.23")
        self.assertEqual(value, 1.23)

        value = rhea_parser.get_float(key='float_key_3', value="123")
        self.assertEqual(value, 123)

        value = rhea_parser.get_float(key='float_list_key_1',
                                      value=[1.23, 13.3, "4.4", "555", 66.0],
                                      is_list=True)
        self.assertEqual(value, [1.23, 13.3, 4.4, 555., 66.])

        value = rhea_parser.get_float(key='float_list_key_1',
                                      value='[1.23, 13.3, "4.4", "555", 66.0]',
                                      is_list=True)
        self.assertEqual(value, [1.23, 13.3, 4.4, 555., 66.])

        with self.assertRaises(RheaError):
            rhea_parser.get_float(key='float_error_key_1', value=None)

        with self.assertRaises(RheaError):
            rhea_parser.get_float(key='float_error_key_1', value='null')

        with self.assertRaises(RheaError):
            rhea_parser.get_float(key='float_error_key_2', value="")

        with self.assertRaises(RheaError):
            rhea_parser.get_float(key='float_error_key_3', value="foo")

        with self.assertRaises(RheaError):
            rhea_parser.get_float(key='float_error_key_4', value=123)

        with self.assertRaises(RheaError):
            rhea_parser.get_float(key='float_list_key_1', value=[1.23, 13.3, "4.4", "555", 66.0])

        with self.assertRaises(RheaError):
            rhea_parser.get_float(key='float_list_error_key_1', value=None, is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_float(key='float_list_error_key_2', value="", is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_float(key='float_list_error_key_3', value="foo", is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_float(key='float_key_1', value=213, is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_float(key='float_key_2', value=[1.23, 13.3, 66], is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_float(key='float_non_existing_key', value=NO_VALUE_FOUND)

        with self.assertRaises(RheaError):
            rhea_parser.get_float(key='float_non_existing_key', value=[1.23, 13.3, "foo"])

        with self.assertRaises(RheaError):
            rhea_parser.get_float(key='float_non_existing_key',
                                  value=[1.23, 13.3, None],
                                  is_list=True)

        self.assertEqual(rhea_parser.get_float(key='float_non_existing_key',
                                               value=None,
                                               is_optional=True), None)
        self.assertEqual(rhea_parser.get_float(key='float_non_existing_key',
                                               value=None,
                                               is_optional=True,
                                               default=3.4), 3.4)

        self.assertEqual(rhea_parser.get_float(key='float_non_existing_key',
                                               value="null",
                                               is_list=True,
                                               is_optional=True), None)
        self.assertEqual(rhea_parser.get_float(key='float_non_existing_key',
                                               value=None,
                                               is_list=True,
                                               is_optional=True,
                                               default=[3.4, 1.2]), [3.4, 1.2])

    def test_get_string(self):
        value = rhea_parser.get_string(key='string_key_1', value="123")
        self.assertEqual(value, "123")

        value = rhea_parser.get_string(key='string_key_2', value="1.23")
        self.assertEqual(value, "1.23")

        value = rhea_parser.get_string(key='string_key_3', value="foo")
        self.assertEqual(value, "foo")

        value = rhea_parser.get_string(key='string_key_4', value="")
        self.assertEqual(value, "")

        value = rhea_parser.get_string(key='string_list_key_1',
                                       value=["123", "1.23", "foo", ""],
                                       is_list=True)
        self.assertEqual(value, ["123", "1.23", "foo", ""])

        value = rhea_parser.get_string(key='string_list_key_1',
                                       value='["123", "1.23", "foo", ""]',
                                       is_list=True)
        self.assertEqual(value, ["123", "1.23", "foo", ""])

        with self.assertRaises(RheaError):
            rhea_parser.get_string(key='string_error_key_1', value=None)

        with self.assertRaises(RheaError):
            rhea_parser.get_string(key='string_error_key_2', value=123)

        with self.assertRaises(RheaError):
            rhea_parser.get_string(key='string_error_key_3', value=1.23)

        with self.assertRaises(RheaError):
            rhea_parser.get_string(key='string_error_key_4', value=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_string(key='string_list_key_1', value=["123", "1.23", "foo", ""])

        with self.assertRaises(RheaError):
            rhea_parser.get_string(key='string_list_error_key_1',
                                   value=["123", 123],
                                   is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_string(key='string_list_error_key_2',
                                   value=["123", 12.3],
                                   is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_string(key='string_list_error_key_3',
                                   value=["123", None],
                                   is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_string(key='string_list_error_key_4',
                                   value=["123", False],
                                   is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_string(key='string_key_3', value="foo", is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_string(key='string_key_4', value="", is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_string(key='string_non_existing_key', value=None)

        with self.assertRaises(RheaError):
            rhea_parser.get_string(key='string_non_existing_key', value=NO_VALUE_FOUND)

        with self.assertRaises(RheaError):
            rhea_parser.get_string(key='string_non_existing_key', value=None, is_list=True)

        self.assertEqual(rhea_parser.get_string(key='string_non_existing_key',
                                                value=None,
                                                is_optional=True), None)
        self.assertEqual(rhea_parser.get_string(key='string_non_existing_key',
                                                value=None,
                                                is_optional=True,
                                                default='foo'), 'foo')

        self.assertEqual(rhea_parser.get_string(key='string_non_existing_key',
                                                value=None,
                                                is_list=True,
                                                is_optional=True), None)
        self.assertEqual(rhea_parser.get_string(key='string_non_existing_key',
                                                value=None,
                                                is_list=True,
                                                is_optional=True,
                                                default=['foo', 'bar']), ['foo', 'bar'])

    def test_get_dict(self):
        value = rhea_parser.get_dict(key='dict_key_1',
                                     value={"key1": "foo", "key2": 2, "key3": False, "key4": "1"})
        self.assertEqual(value, {"key1": "foo", "key2": 2, "key3": False, "key4": "1"})

        value = rhea_parser.get_dict(key='dict_key_1',
                                     value='{"key1": "foo", "key2": 2, "key3": false, "key4": "1"}')
        self.assertEqual(value, {"key1": "foo", "key2": 2, "key3": False, "key4": "1"})

        value = rhea_parser.get_dict(
            key='dict_key_1',
            value="{\"key1\": \"foo\", \"key2\": 2, \"key3\": false, \"key4\": \"1\"}")
        self.assertEqual(value, {"key1": "foo", "key2": 2, "key3": False, "key4": "1"})

        value = rhea_parser.get_dict(key='dict_list_key_1',
                                     value=[
                                         {"key1": "foo", "key2": 2, "key3": False, "key4": "1"},
                                         {"key3": True, "key4": "2"},
                                         {"key1": False, "key2": "3"}],
                                     is_list=True)
        self.assertEqual(value, [
            {"key1": "foo", "key2": 2, "key3": False, "key4": "1"},
            {"key3": True, "key4": "2"},
            {"key1": False, "key2": "3"}
        ])

        with self.assertRaises(RheaError):
            rhea_parser.get_dict(key='dict_error_key_1', value="foo")

        with self.assertRaises(RheaError):
            rhea_parser.get_dict(key='dict_error_key_2', value=1)

        with self.assertRaises(RheaError):
            rhea_parser.get_dict(key='dict_error_key_3', value=False)

        with self.assertRaises(RheaError):
            rhea_parser.get_dict(key='dict_error_key_4', value=["1", "foo"])

        with self.assertRaises(RheaError):
            rhea_parser.get_dict(key='dict_list_key_1', value=["123", {"key3": True}])

        with self.assertRaises(RheaError):
            rhea_parser.get_dict(key='dict_list_error_key_1',
                                 value=["123", {"key3": True}],
                                 is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_dict(key='dict_list_error_key_2',
                                 value=[{"key3": True}, 12.3],
                                 is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_dict(key='dict_list_error_key_3',
                                 value=[{"key3": True}, None],
                                 is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_dict(key='dict_list_error_key_4',
                                 value=[{"key3": True}, "123", False],
                                 is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_dict(key='dict_key_1',
                                 value={"key1": "foo", "key2": 2, "key3": False, "key4": "1"},
                                 is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_dict(key='dict_non_existing_key', value=None)

        with self.assertRaises(RheaError):
            rhea_parser.get_dict(key='dict_non_existing_key', value=NO_VALUE_FOUND)

        with self.assertRaises(RheaError):
            rhea_parser.get_dict(key='dict_non_existing_key', value=None, is_list=True)

        self.assertEqual(
            rhea_parser.get_dict(key='dict_non_existing_key', value=None, is_optional=True), None)
        self.assertEqual(rhea_parser.get_dict(key='dict_non_existing_key',
                                              value=None,
                                              is_optional=True,
                                              default={'foo': 'bar'}), {'foo': 'bar'})

        self.assertEqual(rhea_parser.get_dict(key='dict_non_existing_key',
                                              value=None,
                                              is_list=True,
                                              is_optional=True), None)
        self.assertEqual(rhea_parser.get_dict(key='dict_non_existing_key',
                                              value=None,
                                              is_list=True,
                                              is_optional=True,
                                              default=[{'foo': 'bar'}, {'foo': 'boo'}]),
                         [{'foo': 'bar'}, {'foo': 'boo'}])

    def test_get_uri(self):
        value = rhea_parser.get_uri(key='uri_key_1', value="user:pass@siteweb.ca")
        self.assertEqual(value, UriSpec("user", "pass", "siteweb.ca"))

        value = rhea_parser.get_uri(key='uri_key_2', value="user2:pass@localhost:8080")
        self.assertEqual(value, UriSpec("user2", "pass", "localhost:8080"))

        value = rhea_parser.get_uri(key='uri_key_3', value="user2:pass@https://quay.io")
        self.assertEqual(value, UriSpec("user2", "pass", "https://quay.io"))

        value = rhea_parser.get_uri(key='uri_list_key_1',
                                    value=[
                                        "user:pass@siteweb.ca",
                                        "user2:pass@localhost:8080",
                                        "user2:pass@https://quay.io"],
                                    is_list=True)
        self.assertEqual(value, [
            UriSpec("user", "pass", "siteweb.ca"),
            UriSpec("user2", "pass", "localhost:8080"),
            UriSpec("user2", "pass", "https://quay.io")
        ])

        with self.assertRaises(RheaError):
            rhea_parser.get_uri(key='uri_error_key_1', value="foo")

        with self.assertRaises(RheaError):
            rhea_parser.get_uri(key='uri_error_key_2', value=1)

        with self.assertRaises(RheaError):
            rhea_parser.get_uri(key='uri_error_key_3', value=False)

        with self.assertRaises(RheaError):
            rhea_parser.get_uri(key='uri_error_key_4', value=["1", "foo"])

        with self.assertRaises(RheaError):
            rhea_parser.get_uri(key='uri_list_key_1',
                                value=[
                                    "user:pass@siteweb.ca",
                                    "user2:pass@localhost:8080",
                                    "user2:pass@https://quay.io"])

        with self.assertRaises(RheaError):
            rhea_parser.get_uri(key='uri_list_error_key_1',
                                value=["123", "user:pass@siteweb.ca"],
                                is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_uri(key='uri_list_error_key_2',
                                value=["user:pass@siteweb.ca", 12.3],
                                is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_uri(key='uri_list_error_key_3',
                                value=["user:pass@siteweb.ca", None],
                                is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_uri(key='uri_list_error_key_4',
                                value=["user:pass@siteweb.ca", "123", False],
                                is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_uri(key='uri_key_1', value="user:pass@siteweb.ca", is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_uri(key='uri_non_existing_key', value=None)

        with self.assertRaises(RheaError):
            rhea_parser.get_uri(key='uri_non_existing_key', value=NO_VALUE_FOUND)

        with self.assertRaises(RheaError):
            rhea_parser.get_uri(key='uri_non_existing_key', value=None, is_list=True)

        self.assertEqual(rhea_parser.get_uri(key='uri_non_existing_key',
                                             value=None,
                                             is_optional=True), None)
        self.assertEqual(
            rhea_parser.get_uri(key='uri_non_existing_key',
                                value=None,
                                is_optional=True,
                                default=UriSpec("user2", "pass", "localhost:8080")),
            UriSpec("user2", "pass", "localhost:8080"))

        self.assertEqual(
            rhea_parser.get_uri(key='uri_non_existing_key',
                                value=None,
                                is_list=True,
                                is_optional=True), None)
        self.assertEqual(
            rhea_parser.get_uri(key='uri_non_existing_key',
                                value=None,
                                is_list=True,
                                is_optional=True,
                                default=[UriSpec("user", "pass", "siteweb.ca"),
                                         UriSpec("user2", "pass", "localhost:8080")]),
            [UriSpec("user", "pass", "siteweb.ca"), UriSpec("user2", "pass", "localhost:8080")])

    def test_get_auth(self):
        value = rhea_parser.get_auth(key='auth_key_1', value="user:pass")
        self.assertEqual(value, AuthSpec("user", "pass"))

        value = rhea_parser.get_auth(key='auth_list_key_1',
                                     value=[
                                         "user:pass",
                                         "user2:pass"],
                                     is_list=True)
        self.assertEqual(value, [
            AuthSpec("user", "pass"),
            AuthSpec("user2", "pass"),
        ])

        with self.assertRaises(RheaError):
            rhea_parser.get_auth(key='auth_error_key_1', value="foo")

        with self.assertRaises(RheaError):
            rhea_parser.get_auth(key='auth_error_key_2', value=1)

        with self.assertRaises(RheaError):
            rhea_parser.get_auth(key='auth_error_key_3', value=False)

        with self.assertRaises(RheaError):
            rhea_parser.get_auth(key='auth_error_key_4', value=["1", "foo"])

        with self.assertRaises(RheaError):
            rhea_parser.get_auth(key='auth_list_key_1',
                                 value=[
                                     "user:pass",
                                     "user2:pass"])

        with self.assertRaises(RheaError):
            rhea_parser.get_auth(key='auth_list_error_key_1',
                                 value=["123", "user:pass"],
                                 is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_auth(key='auth_list_error_key_2',
                                 value=["user:pass", 12.3],
                                 is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_auth(key='auth_list_error_key_3',
                                 value=["user:pass", None],
                                 is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_auth(key='auth_list_error_key_4',
                                 value=["user:pass", "123", False],
                                 is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_auth(key='auth_key_1',
                                 value="user:pass",
                                 is_list=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_auth(key='auth_non_existing_key', value=None)

        with self.assertRaises(RheaError):
            rhea_parser.get_auth(key='auth_non_existing_key', value=NO_VALUE_FOUND)

        with self.assertRaises(RheaError):
            rhea_parser.get_auth(key='auth_non_existing_key', value=None, is_list=True)

        self.assertEqual(
            rhea_parser.get_auth(key='auth_non_existing_key', value=None, is_optional=True), None)
        self.assertEqual(
            rhea_parser.get_auth(key='auth_non_existing_key',
                                 value=None,
                                 is_optional=True,
                                 default=AuthSpec("user2", "pass")),
            AuthSpec("user2", "pass"))

        self.assertEqual(
            rhea_parser.get_auth(key='auth_non_existing_key',
                                 value=None,
                                 is_list=True,
                                 is_optional=True), None)
        self.assertEqual(
            rhea_parser.get_auth(key='auth_non_existing_key',
                                 value=None,
                                 is_list=True,
                                 is_optional=True,
                                 default=[AuthSpec("user", "pass"),
                                          AuthSpec("user2", "pass")]),
            [AuthSpec("user", "pass"), AuthSpec("user2", "pass")])

    def test_get_list(self):
        value = rhea_parser.get_list(key='list_key_1',
                                     value="user:pass@siteweb.ca, 'pp', 0.1, 'foo'")
        self.assertEqual(value, ['user:pass@siteweb.ca', "'pp'", '0.1', "'foo'"])

        value = rhea_parser.get_list(key='list_key_2',
                                     value="user1,user2 , user3,     user4    , user5")
        self.assertEqual(value, ['user1', 'user2', 'user3', 'user4', 'user5'])

        value = rhea_parser.get_list(key='list_key_3', value=[False])
        self.assertEqual(value, [False])

        value = rhea_parser.get_list(key='list_key_3', value=['false'])
        self.assertEqual(value, ['false'])

        value = rhea_parser.get_list(key='list_key_4', value="foo")
        self.assertEqual(value, ['foo'])

        value = rhea_parser.get_list(key='list_key_5', value="")
        self.assertEqual(value, [])

        value = rhea_parser.get_list(key='list_error_key_3', value='null')
        self.assertEqual(value, ['null'])

        with self.assertRaises(RheaError):
            rhea_parser.get_list(key='list_error_key_1', value=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_list(key='list_error_key_2', value={"key": "value"})

        with self.assertRaises(RheaError):
            rhea_parser.get_list(key='list_error_key_4', value=123)

        with self.assertRaises(RheaError):
            rhea_parser.get_list(key='list_non_existing_key', value=None)

        with self.assertRaises(RheaError):
            rhea_parser.get_list(key='list_non_existing_key', value=NO_VALUE_FOUND)

        self.assertEqual(rhea_parser.get_list(key='list_non_existing_key',
                                              value=None,
                                              is_optional=True), None)
        self.assertEqual(rhea_parser.get_list(key='list_non_existing_key',
                                              value=None,
                                              is_optional=True,
                                              default=['foo']), ['foo'])

    def test_get_dict_of_dicts(self):
        value = rhea_parser.get_dict_of_dicts(
            key='dict_dicts_key_1',
            value={"data1": {"mountPath": "/data/21", "existingClaim": "data-1-pvc"}})
        self.assertEqual(value, {'data1': {'mountPath': '/data/21', 'existingClaim': 'data-1-pvc'}})

        value = rhea_parser.get_dict_of_dicts(
            key='dict_dicts_key_1',
            value='{"data1": {"mountPath": "/data/21", "existingClaim": "data-1-pvc"}}')
        self.assertEqual(value, {'data1': {'mountPath': '/data/21', 'existingClaim': 'data-1-pvc'}})

        value = rhea_parser.get_dict_of_dicts(
            key='dict_dicts_key_2',
            value={
                "outputs1": {"mountPath": "/output/2", "existingClaim": "outputs-1-pvc"},
                "outputs2": {"mountPath": "/output/2", "existingClaim": "output-2-pvc"}})
        self.assertEqual(value, {
            'outputs1': {'mountPath': '/output/2', 'existingClaim': 'outputs-1-pvc'},
            'outputs2': {'mountPath': '/output/2', 'existingClaim': 'output-2-pvc'}})

        value = rhea_parser.get_dict_of_dicts(key='dict_dicts_key_3', value={})
        self.assertEqual(value, None)

        with self.assertRaises(RheaError):
            rhea_parser.get_dict_of_dicts(key='dict_dicts_error_key_1', value=True)

        with self.assertRaises(RheaError):
            rhea_parser.get_dict_of_dicts(key='dict_dicts_error_key_2', value={"key": "value"})

        with self.assertRaises(RheaError):
            rhea_parser.get_dict_of_dicts(key='dict_dicts_error_key_3', value='null')

        with self.assertRaises(RheaError):
            rhea_parser.get_dict_of_dicts(key='dict_dicts_error_key_4', value=123)

        with self.assertRaises(RheaError):
            rhea_parser.get_dict_of_dicts(key='dict_dicts_error_key_5', value="foo")

        with self.assertRaises(RheaError):
            rhea_parser.get_dict_of_dicts(key='dict_dicts_error_key_6', value="")

        with self.assertRaises(RheaError):
            rhea_parser.get_dict_of_dicts(
                key='dict_dicts_error_key_7',
                value={"mountPath": "/data/2", "existingClaim": "data-2-pvc"})

        with self.assertRaises(RheaError):
            rhea_parser.get_dict_of_dicts(key='dict_dicts_non_existing_key', value=None)

        with self.assertRaises(RheaError):
            rhea_parser.get_dict_of_dicts(key='dict_dicts_non_existing_key', value=NO_VALUE_FOUND)

        self.assertEqual(rhea_parser.get_dict_of_dicts(key='dict_dicts_non_existing_key',
                                                       value=None,
                                                       is_optional=True), None)
        self.assertEqual(rhea_parser.get_dict_of_dicts(key='dict_dicts_non_existing_key',
                                                       value=None,
                                                       is_optional=True, default={}), {})

    def test_get_wasbs_path(self):
        # Correct url
        wasbs_path = 'wasbs://container@user.blob.core.windows.net/path'
        parsed_url = rhea_parser.parse_wasbs_path(wasbs_path)
        assert parsed_url == WasbsSpec('container', 'user', 'path')
        wasbs_path = 'wasbs://container@user.blob.core.windows.net/'
        parsed_url = rhea_parser.parse_wasbs_path(wasbs_path)
        assert parsed_url == WasbsSpec('container', 'user', '')
        wasbs_path = 'wasbs://container@user.blob.core.windows.net'
        parsed_url = rhea_parser.parse_wasbs_path(wasbs_path)
        assert parsed_url == WasbsSpec('container', 'user', '')
        wasbs_path = 'wasbs://container@user.blob.core.windows.net/path/to/file'
        parsed_url = rhea_parser.parse_wasbs_path(wasbs_path)
        assert parsed_url == WasbsSpec('container', 'user', 'path/to/file')

        # Wrong url
        wasbs_path = 'wasbs://container@user.foo.bar.windows.net/path/to/file'
        with self.assertRaises(RheaError):
            rhea_parser.parse_wasbs_path(wasbs_path)

        wasbs_path = 'wasbs://container@user.blob.core.foo.net/path/to/file'
        with self.assertRaises(RheaError):
            rhea_parser.parse_wasbs_path(wasbs_path)

        wasbs_path = 'wasbs://container@user.blob.windows.net/path/to/file'
        with self.assertRaises(RheaError):
            rhea_parser.parse_wasbs_path(wasbs_path)

    def test_parse_gcs_path(self):
        # Correct url
        gcs_path = 'gs://bucket/path/to/blob'
        parsed_url = rhea_parser.parse_gcs_path(gcs_path)
        assert parsed_url == GCSSpec('bucket', 'path/to/blob')

        # Wrong url
        gcs_path = 'gs:/bucket/path/to/blob'
        with self.assertRaises(RheaError):
            rhea_parser.parse_gcs_path(gcs_path)

        # Trailing slash
        gcs_path = 'gs://bucket/path/to/blob/'
        assert rhea_parser.parse_gcs_path(gcs_path) == GCSSpec('bucket', 'path/to/blob/')

        # Bucket only
        gcs_path = 'gs://bucket/'
        assert rhea_parser.parse_gcs_path(gcs_path) == GCSSpec('bucket', '')

    def test_parse_s3_path(self):
        s3_path = 's3://test/this/is/bad/key.txt'
        parsed_url = rhea_parser.parse_s3_path(s3_path)
        assert parsed_url == S3Spec('test', 'this/is/bad/key.txt')
