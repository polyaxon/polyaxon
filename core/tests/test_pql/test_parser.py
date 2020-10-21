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

from polyaxon.exceptions import PQLException
from polyaxon.pql.parser import (
    QueryOpSpec,
    parse_datetime_operation,
    parse_expression,
    parse_field,
    parse_negation_operation,
    parse_scalar_operation,
    parse_value_operation,
    split_query,
    tokenize_query,
)
from tests.utils import BaseTestCase


class TestParser(BaseTestCase):
    def test_base_parser_raises_for_invalid_expressions(self):
        with self.assertRaises(PQLException):
            parse_expression("foo:bar:moo")

        with self.assertRaises(PQLException):
            parse_expression("foo")

        with self.assertRaises(PQLException):
            parse_expression(None)

        with self.assertRaises(PQLException):
            parse_expression(12)

        with self.assertRaises(PQLException):
            parse_expression("fff:")

        with self.assertRaises(PQLException):
            parse_expression(":dsf")

        with self.assertRaises(PQLException):
            parse_expression(":")

    def test_base_parser_passes_for_valid_expressions(self):
        assert parse_expression("foo:bar") == ("foo", "bar")
        assert parse_expression("foo:>=bar") == ("foo", ">=bar")
        assert parse_expression("foo:bar|moo|boo") == ("foo", "bar|moo|boo")
        assert parse_expression("foo:bar..moo") == ("foo", "bar..moo")
        assert parse_expression("foo:~bar") == ("foo", "~bar")

        # Handles spaces
        assert parse_expression(" foo: bar ") == ("foo", "bar")
        assert parse_expression("foo :>=bar ") == ("foo", ">=bar")
        assert parse_expression(" foo :bar|moo|boo") == ("foo", "bar|moo|boo")
        assert parse_expression(" foo : bar..moo ") == ("foo", "bar..moo")
        assert parse_expression(" foo : ~bar ") == ("foo", "~bar")

    def test_parse_negation_operation(self):
        assert parse_negation_operation("foo") == (False, "foo")
        assert parse_negation_operation("~foo") == (True, "foo")
        assert parse_negation_operation("foo..boo") == (False, "foo..boo")
        assert parse_negation_operation("~foo..boo") == (True, "foo..boo")
        assert parse_negation_operation(">=foo") == (False, ">=foo")
        assert parse_negation_operation("~>=foo") == (True, ">=foo")
        assert parse_negation_operation("foo|boo") == (False, "foo|boo")
        assert parse_negation_operation("~foo|boo") == (True, "foo|boo")
        assert parse_negation_operation(" ~ >=foo ") == (True, ">=foo")
        assert parse_negation_operation(" foo|boo ") == (False, "foo|boo")
        assert parse_negation_operation("~ foo|boo") == (True, "foo|boo")

    def test_parse_datetime_operation(self):
        # Raises for not allowed operators
        with self.assertRaises(PQLException):
            parse_datetime_operation("foo|bar")

        with self.assertRaises(PQLException):
            parse_datetime_operation("")

        with self.assertRaises(PQLException):
            parse_datetime_operation("~")

        with self.assertRaises(PQLException):
            parse_datetime_operation("..")

        with self.assertRaises(PQLException):
            parse_datetime_operation("..da")

        with self.assertRaises(PQLException):
            parse_datetime_operation("asd..")

        with self.assertRaises(PQLException):
            parse_datetime_operation("asd..asd..asd")

        # Parses ranges
        assert parse_datetime_operation("foo..bar") == (
            QueryOpSpec("..", False, ["foo", "bar"])
        )
        assert parse_datetime_operation(" foo .. bar ") == (
            QueryOpSpec("..", False, ["foo", "bar"])
        )
        assert parse_datetime_operation("~ foo .. bar ") == (
            QueryOpSpec("..", True, ["foo", "bar"])
        )

        # Comparison
        assert parse_datetime_operation(">=foo") == (QueryOpSpec(">=", False, "foo"))
        assert parse_datetime_operation(" ~ <= bar ") == (
            QueryOpSpec("<=", True, "bar")
        )
        assert parse_datetime_operation("~ > bar ") == (QueryOpSpec(">", True, "bar"))

        # Equality
        assert parse_datetime_operation("foo") == (QueryOpSpec("=", False, "foo"))
        assert parse_datetime_operation(" ~  bar ") == (QueryOpSpec("=", True, "bar"))
        assert parse_datetime_operation("~bar") == (QueryOpSpec("=", True, "bar"))

    def test_parse_scalar_operation(self):
        # Raises for not allowed operators
        with self.assertRaises(PQLException):
            parse_scalar_operation("1|12")

        with self.assertRaises(PQLException):
            parse_scalar_operation("0.1..0.2")

        # Raise for not scalars
        with self.assertRaises(PQLException):
            parse_scalar_operation(">=f")

        with self.assertRaises(PQLException):
            parse_scalar_operation(" ~ <=f1 ")

        with self.assertRaises(PQLException):
            parse_scalar_operation("~ > bbb ")

        with self.assertRaises(PQLException):
            parse_datetime_operation("")

        with self.assertRaises(PQLException):
            parse_datetime_operation("~")

        with self.assertRaises(PQLException):
            parse_datetime_operation(">")

        # Comparison
        assert parse_scalar_operation(">=1") == (QueryOpSpec(">=", False, 1))
        assert parse_scalar_operation(" ~ <= 0.1 ") == (QueryOpSpec("<=", True, 0.1))
        assert parse_scalar_operation("~ > 20 ") == (QueryOpSpec(">", True, 20))

        # Equality
        assert parse_scalar_operation("1") == (QueryOpSpec("=", False, 1))
        assert parse_scalar_operation(" ~  2 ") == (QueryOpSpec("=", True, 2))
        assert parse_scalar_operation("~0.1") == (QueryOpSpec("=", True, 0.1))

    def test_parse_value_operation(self):
        # Raises for not allowed operators
        with self.assertRaises(PQLException):
            parse_value_operation("0.1..0.2")

        with self.assertRaises(PQLException):
            parse_datetime_operation("")

        with self.assertRaises(PQLException):
            parse_datetime_operation("~")

        # Raises for comparison
        with self.assertRaises(PQLException):
            parse_value_operation(">=f")

        with self.assertRaises(PQLException):
            parse_value_operation(" ~ <=f1 ")

        with self.assertRaises(PQLException):
            parse_value_operation("~|")

        with self.assertRaises(PQLException):
            parse_value_operation("|")

        with self.assertRaises(PQLException):
            parse_value_operation("~tag1 |")

        # Equality
        assert parse_value_operation("tag") == (QueryOpSpec("=", False, "tag"))
        assert parse_value_operation(" ~  tag ") == (QueryOpSpec("=", True, "tag"))
        assert parse_value_operation("~tag") == (QueryOpSpec("=", True, "tag"))

        # In op
        assert parse_value_operation("tag1|tag2") == (
            QueryOpSpec("|", False, ["tag1", "tag2"])
        )
        assert parse_value_operation(" ~  tag1|tag2 ") == (
            QueryOpSpec("|", True, ["tag1", "tag2"])
        )
        assert parse_value_operation("~tag1 | tag2| tag23") == (
            QueryOpSpec("|", True, ["tag1", "tag2", "tag23"])
        )

    def test_split_query(self):
        with self.assertRaises(PQLException):
            split_query("")

        with self.assertRaises(PQLException):
            split_query(",")

        with self.assertRaises(PQLException):
            split_query(", , ")

        assert len(split_query("name:~tag1 | tag2| tag23")) == 1
        assert len(split_query("name:~tag1 | tag2| tag23, name2:foo")) == 2

    def test_tokenize_query(self):
        with self.assertRaises(PQLException):
            tokenize_query("")

        with self.assertRaises(PQLException):
            tokenize_query(",")

        with self.assertRaises(PQLException):
            tokenize_query(", , ")

        assert tokenize_query("name:~tag1 | tag2| tag23") == {
            "name": ["~tag1 | tag2| tag23"]
        }
        assert tokenize_query(
            "name1:~tag1 | tag2| tag23, name1:foo, name2:sdf..dsf"
        ) == {"name1": ["~tag1 | tag2| tag23", "foo"], "name2": ["sdf..dsf"]}

    def test_parse_field(self):
        with self.assertRaises(PQLException):
            parse_field("")

        with self.assertRaises(PQLException):
            parse_field(".")

        with self.assertRaises(PQLException):
            parse_field("sdf.sdf.sf")

        with self.assertRaises(PQLException):
            parse_field("foo.")

        assert parse_field("foo") == ("foo", None)
        assert parse_field("foo_bar") == ("foo_bar", None)
        assert parse_field("foo.bar") == ("foo", "bar")
        assert parse_field("metric.foo_bar") == ("metric", "foo_bar")
