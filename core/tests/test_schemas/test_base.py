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


from marshmallow import Schema, ValidationError, fields

from polyaxon.schemas.base import BaseConfig, BaseOneOfSchema, BaseSchema
from tests.utils import BaseTestCase

REQUIRED_ERROR = u"Missing data for required field."


class FooSchema(BaseSchema):
    value = fields.String(required=True)

    @staticmethod
    def schema_config():
        return FooConfig


class FooConfig(BaseConfig):
    SCHEMA = FooSchema
    IDENTIFIER = "foo"

    def __init__(self, value=None):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.value == other.value


class BarSchema(BaseSchema):
    value = fields.Integer(required=True)

    @staticmethod
    def schema_config():
        return BarConfig


class BarConfig(BaseConfig):
    SCHEMA = BarSchema
    IDENTIFIER = "bar"

    def __init__(self, value=None):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.value == other.value


class BazSchema(BaseSchema):
    value1 = fields.Integer(required=True)
    value2 = fields.String(required=True)

    @staticmethod
    def schema_config():
        return BazConfig


class BazConfig(BaseConfig):
    SCHEMA = BazSchema
    IDENTIFIER = "baz"

    def __init__(self, value1=None, value2=None):
        self.value1 = value1
        self.value2 = value2

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.value1 == other.value1
            and self.value2 == other.value2
        )


class EmptySchema(BaseSchema):
    @staticmethod
    def schema_config():
        return EmptyConfig


class EmptyConfig(BaseConfig):
    SCHEMA = EmptySchema
    IDENTIFIER = "empty"


class MySchema(BaseOneOfSchema):
    SCHEMAS = {
        "foo": FooSchema,
        "bar": BarSchema,
        "baz": BazSchema,
        "empty": EmptySchema,
    }


class TestOneOfSchema(BaseTestCase):
    def test_dump(self):
        foo_result = MySchema().dump(FooConfig("hello"))
        assert {"type": "foo", "value": "hello"} == foo_result

        bar_result = MySchema().dump(BarConfig(123))
        assert {"type": "bar", "value": 123} == bar_result

    def test_dump_many(self):
        result = MySchema().dump([FooConfig("hello"), BarConfig(123)], many=True)
        assert [
            {"type": "foo", "value": "hello"},
            {"type": "bar", "value": 123},
        ] == result

    def test_dump_many_in_constructor(self):
        result = MySchema(many=True).dump([FooConfig("hello"), BarConfig(123)])
        assert [
            {"type": "foo", "value": "hello"},
            {"type": "bar", "value": 123},
        ] == result

    def test_dump_with_empty_keeps_type(self):
        result = MySchema().dump(EmptyConfig())
        assert {"type": "empty"} == result

    def test_load(self):
        foo_result = MySchema().load({"type": "foo", "value": "world"})
        assert FooConfig("world") == foo_result

        bar_result = MySchema().load({"type": "bar", "value": 456})
        assert BarConfig(456) == bar_result

    def test_load_many(self):
        result = MySchema().load(
            [{"type": "foo", "value": "hello world!"}, {"type": "bar", "value": 123}],
            many=True,
        )
        assert FooConfig("hello world!"), BarConfig(123) == result

    def test_load_many_in_constructor(self):
        result = MySchema(many=True).load(
            [{"type": "foo", "value": "hello world!"}, {"type": "bar", "value": 123}]
        )
        assert FooConfig("hello world!"), BarConfig(123) == result

    def test_load_removes_type_field(self):
        class Nonlocal:
            data = None

        class MySchema(Schema):
            def load(self, data, *args, **kwargs):
                Nonlocal.data = data
                return super().load(data, *args, **kwargs)

        class FooSchema(MySchema):
            foo = fields.String(required=True)

        class BarSchema(MySchema):
            bar = fields.Integer(required=True)

        class TestSchema(BaseOneOfSchema):
            SCHEMAS = {"foo": FooSchema, "bar": BarSchema}

        TestSchema().load({"type": "foo", "foo": "hello"})
        assert "type" not in Nonlocal.data

        TestSchema().load({"type": "bar", "bar": 123})
        assert "type" not in Nonlocal.data

    def test_load_keeps_type_field(self):
        class Nonlocal:
            data = None
            type = None

        class MySchema(Schema):
            def load(self, data, *args, **kwargs):
                Nonlocal.data = data
                return super().load(data, *args, **kwargs)

        class FooSchema(MySchema):
            foo = fields.String(required=True)

        class BarSchema(MySchema):
            bar = fields.Integer(required=True)

        class TestSchema(BaseOneOfSchema):
            TYPE_FIELD_REMOVE = False
            SCHEMAS = {"foo": FooSchema, "bar": BarSchema}

        TestSchema(unknown="exclude").load({"type": "foo", "foo": "hello"})
        assert Nonlocal.data["type"] == "foo"

        TestSchema(unknown="exclude").load({"type": "bar", "bar": 123})
        assert Nonlocal.data["type"] == "bar"

    def test_load_non_dict(self):
        with self.assertRaises(ValidationError):
            MySchema().load(123)

        with self.assertRaises(ValidationError):
            MySchema().load("foo")

    def test_load_errors_no_type(self):
        with self.assertRaises(ValidationError):
            MySchema().load({"value": "foo"})

    def test_load_errors_field_error(self):
        with self.assertRaises(ValidationError):
            MySchema().load({"type": "foo"})

    def test_load_errors_strict(self):
        with self.assertRaises(ValidationError):
            MySchema().load({"type": "foo"})

    def test_load_many_errors_are_indexed_by_object_position(self):
        with self.assertRaises(ValidationError):
            MySchema().load([{"type": "foo"}, {"type": "bar", "value": 123}], many=True)

    def test_load_many_errors_strict(self):
        with self.assertRaises(ValidationError):
            MySchema().load(
                [
                    {"type": "foo", "value": "hello world!"},
                    {"type": "foo"},
                    {"type": "bar", "value": 123},
                    {"type": "bar", "value": "hello"},
                ],
                many=True,
            )

    def test_load_partial_specific(self):
        result = MySchema().load({"type": "foo"}, partial=("value", "value2"))
        assert FooConfig() == result

        result = MySchema().load(
            {"type": "baz", "value1": 123}, partial=("value", "value2")
        )
        assert BazConfig(value1=123) == result

    def test_load_partial_any(self):
        result = MySchema().load({"type": "foo"}, partial=True)
        assert FooConfig() == result

        result = MySchema().load({"type": "baz", "value1": 123}, partial=True)
        assert BazConfig(value1=123) == result

        result = MySchema().load({"type": "baz", "value2": "hello"}, partial=True)
        assert BazConfig(value2="hello") == result

    def test_load_partial_specific_in_constructor(self):
        result = MySchema(partial=("value", "value2")).load({"type": "foo"})
        assert FooConfig() == result

        result = MySchema(partial=("value", "value2")).load(
            {"type": "baz", "value1": 123}
        )
        assert BazConfig(value1=123) == result

    def test_load_partial_any_in_constructor(self):
        result = MySchema(partial=True).load({"type": "foo"})
        assert FooConfig() == result

        result = MySchema(partial=True).load({"type": "baz", "value1": 123})
        assert BazConfig(value1=123) == result

        result = MySchema(partial=True).load({"type": "baz", "value2": "hello"})
        assert BazConfig(value2="hello") == result

    def test_validate(self):
        assert {} == MySchema().validate({"type": "foo", "value": "123"})
        assert {0: {"value": [REQUIRED_ERROR]}} == MySchema().validate({"type": "bar"})
        assert {0: {"value": [REQUIRED_ERROR]}} == MySchema().validate({"type": "bar"})

    def test_validate_many(self):
        errors = MySchema().validate(
            [{"type": "foo", "value": "123"}, {"type": "bar", "value": 123}], many=True
        )
        assert {} == errors

        errors = MySchema().validate([{"value": "123"}, {"type": "bar"}], many=True)
        assert {0: {"type": [REQUIRED_ERROR]}, 1: {"value": [REQUIRED_ERROR]}} == errors

        errors = MySchema().validate([{"value": "123"}, {"type": "bar"}], many=True)
        assert {0: {"type": [REQUIRED_ERROR]}, 1: {"value": [REQUIRED_ERROR]}} == errors

    def test_validate_many_in_constructor(self):
        errors = MySchema(many=True).validate(
            [{"type": "foo", "value": "123"}, {"type": "bar", "value": 123}]
        )
        assert {} == errors

        errors = MySchema(many=True).validate([{"value": "123"}, {"type": "bar"}])
        assert {0: {"type": [REQUIRED_ERROR]}, 1: {"value": [REQUIRED_ERROR]}} == errors

    def test_validate_partial_specific(self):
        errors = MySchema().validate({"type": "foo"}, partial=("value", "value2"))
        assert {} == errors

        errors = MySchema().validate(
            {"type": "baz", "value1": 123}, partial=("value", "value2")
        )
        assert {} == errors

    def test_validate_partial_any(self):
        errors = MySchema().validate({"type": "foo"}, partial=True)
        assert {} == errors

        errors = MySchema().validate({"type": "baz", "value1": 123}, partial=True)
        assert {} == errors

        errors = MySchema().validate({"type": "baz", "value2": "hello"}, partial=True)
        assert {} == errors

    def test_validate_partial_specific_in_constructor(self):
        errors = MySchema(partial=("value", "value2")).validate({"type": "foo"})
        assert {} == errors

        errors = MySchema(partial=("value", "value2")).validate(
            {"type": "baz", "value1": 123}
        )
        assert {} == errors

    def test_validate_partial_any_in_constructor(self):
        errors = MySchema(partial=True).validate({"type": "foo"})
        assert {} == errors

        errors = MySchema(partial=True).validate({"type": "baz", "value1": 123})
        assert {} == errors

        errors = MySchema(partial=True).validate({"type": "baz", "value2": "hello"})
        assert {} == errors

    def test_using_as_nested_schema(self):
        class SchemaWithList(Schema):
            items = fields.List(fields.Nested(MySchema))

        schema = SchemaWithList()
        result = schema.load(
            {
                "items": [
                    {"type": "foo", "value": "hello world!"},
                    {"type": "bar", "value": 123},
                ]
            }
        )
        assert {"items": [FooConfig("hello world!"), BarConfig(123)]} == result

        with self.assertRaises(ValidationError):
            schema.load(
                {"items": [{"type": "foo", "value": "hello world!"}, {"value": 123}]}
            )

    def test_using_as_nested_schema_with_many(self):
        class SchemaWithMany(Schema):
            items = fields.Nested(MySchema, many=True)

        schema = SchemaWithMany()
        result = schema.load(
            {
                "items": [
                    {"type": "foo", "value": "hello world!"},
                    {"type": "bar", "value": 123},
                ]
            }
        )
        assert {"items": [FooConfig("hello world!"), BarConfig(123)]} == result

        with self.assertRaises(ValidationError):
            schema.load(
                {"items": [{"type": "foo", "value": "hello world!"}, {"value": 123}]}
            )

    def test_using_custom_type_field(self):
        class MyCustomTypeFieldSchema(MySchema):
            TYPE_FIELD = "object_type"

        schema = MyCustomTypeFieldSchema()
        data = [FooConfig("hello"), BarConfig(111)]
        marshalled = schema.dump(data, many=True)
        assert [
            {"object_type": "foo", "value": "hello"},
            {"object_type": "bar", "value": 111},
        ] == marshalled

        unmarshalled = schema.load(marshalled, many=True)
        assert data == unmarshalled
