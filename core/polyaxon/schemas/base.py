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

from collections import OrderedDict
from collections.abc import Mapping
from datetime import timezone

import ujson

from marshmallow import RAISE, Schema, ValidationError, post_dump, post_load
from marshmallow.utils import EXCLUDE

from polyaxon import pkg
from polyaxon.config_reader.spec import ConfigSpec
from polyaxon.exceptions import PolyaxonSchemaError
from polyaxon.schemas.utils import to_camel_case
from polyaxon.utils.humanize import humanize_timesince
from polyaxon.utils.list_utils import to_list
from polyaxon.utils.tz_utils import get_timezone
from polyaxon.utils.units import to_percentage, to_unit_memory


class BaseSchema(Schema):
    """Base schema."""

    class Meta:
        unknown = RAISE
        ordered = True
        render_module = ujson

    @post_load
    def make(self, data, **kwargs):
        return self.schema_config()(**data)

    @post_dump
    def unmake(self, data, **kwargs):
        return self.schema_config().remove_reduced_attrs(data)

    @staticmethod
    def schema_config():
        raise NotImplementedError


class BaseCamelSchema(BaseSchema):
    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = to_camel_case(field_obj.data_key or field_name)


class BaseConfig:
    """Base for config classes."""

    SCHEMA = None
    IDENTIFIER = None
    REDUCED_ATTRIBUTES = []  # Attribute to remove in the reduced form if they are null.
    DEFAULT_INCLUDE_ATTRIBUTES = []
    DEFAULT_EXCLUDE_ATTRIBUTES = []
    DATETIME_ATTRIBUTES = []
    MEM_SIZE_ATTRIBUTES = []
    PERCENT_ATTRIBUTES = []
    ROUNDING = 2
    UNKNOWN_BEHAVIOUR = RAISE
    WRITE_MODE = 0o777

    def to_light_dict(
        self,
        humanize_values=False,
        include_attrs=None,
        exclude_attrs=None,
        unknown=None,
        dump=False,
    ):
        unknown = unknown or self.UNKNOWN_BEHAVIOUR
        obj_dict = self.to_dict(humanize_values=humanize_values, unknown=unknown)
        if all([include_attrs, exclude_attrs]):
            raise PolyaxonSchemaError(
                "Only one value `include_attrs` or `exclude_attrs` is allowed."
            )
        if not any([include_attrs, exclude_attrs]):  # Use Default setup attrs
            include_attrs = self.DEFAULT_INCLUDE_ATTRIBUTES
            exclude_attrs = self.DEFAULT_EXCLUDE_ATTRIBUTES

        if include_attrs:
            exclude_attrs = set(obj_dict.keys()) - set(include_attrs)
        for attr in exclude_attrs:
            obj_dict.pop(attr, None)

        if dump:
            return ujson.dumps(obj_dict)
        return obj_dict

    def to_dict(
        self,
        humanize_values=False,
        unknown=None,
        dump=False,
        include_kind=False,
        include_version=False,
    ):
        unknown = unknown or self.UNKNOWN_BEHAVIOUR
        obj = self.obj_to_dict(
            self,
            humanize_values=humanize_values,
            unknown=unknown,
            include_kind=include_kind,
            include_version=include_version,
        )
        if dump:
            return ujson.dumps(obj)
        return obj

    def to_schema(self):
        return self.obj_to_schema(self)

    @classmethod
    def humanize_attrs(cls, obj):
        humanized_attrs = {}
        for attr in cls.DATETIME_ATTRIBUTES:
            humanized_attrs[attr] = humanize_timesince(getattr(obj, attr))
        for attr in cls.PERCENT_ATTRIBUTES:
            humanized_attrs[attr] = to_percentage(getattr(obj, attr), cls.ROUNDING)
        for attr in cls.MEM_SIZE_ATTRIBUTES:
            humanized_attrs[attr] = to_unit_memory(getattr(obj, attr))
        return humanized_attrs

    @classmethod
    def obj_to_dict(
        cls,
        obj,
        humanize_values=False,
        unknown=None,
        include_kind=False,
        include_version=False,
    ):
        unknown = unknown or cls.UNKNOWN_BEHAVIOUR
        humanized_attrs = cls.humanize_attrs(obj) if humanize_values else {}
        data_dict = cls.SCHEMA(unknown=unknown).dump(  # pylint: disable=not-callable
            obj
        )

        if include_kind and "kind" not in data_dict and hasattr(obj, "kind"):
            data_dict["kind"] = obj.IDENTIFIER

        if include_version and "version" not in data_dict:
            data_dict["version"] = pkg.SCHEMA_VERSION

        for k, v in humanized_attrs.items():
            data_dict[k] = v
        return data_dict

    @classmethod
    def remove_reduced_attrs(cls, data):
        obj_dict = OrderedDict((key, value) for (key, value) in data.items())
        for attr in cls.REDUCED_ATTRIBUTES:
            if obj_dict[attr] is None:
                del obj_dict[attr]

        return obj_dict

    @classmethod
    def obj_to_schema(cls, obj):
        return {cls.IDENTIFIER: cls.obj_to_dict(obj)}

    @classmethod
    def from_dict(cls, value, unknown=None):
        unknown = unknown or cls.UNKNOWN_BEHAVIOUR
        return cls.SCHEMA(unknown=unknown).load(value)  # pylint: disable=not-callable

    @classmethod
    def read(cls, values, unknown=None, config_type=None):
        values = ConfigSpec.read_from(values, config_type=config_type)
        return cls.from_dict(values, unknown=unknown)

    @classmethod
    def init_file(cls, filepath: str, config=None):
        if not os.path.exists(filepath):
            cls.write(config or cls(), filepath=filepath)
            os.chmod(filepath, cls.WRITE_MODE)

    def write(self, filepath: str):
        with open(filepath, "w") as config_file:
            config_file.write(self.to_dict(dump=True))

    @classmethod
    def patch_obj(cls, config, values):
        values = [config.to_dict()] + to_list(values)
        return cls.read(values=values)

    def patch(self, values):
        return self.patch_obj(self, values)

    @staticmethod
    def localize_date(dt):
        if not dt:
            return dt
        if not dt.tzinfo:
            dt = timezone.utc.localize(dt)
        return dt.astimezone(get_timezone())

    @classmethod
    def to_jsonschema(cls):
        from marshmallow_jsonschema import JSONSchema  # pylint:disable=import-error

        return JSONSchema().dump(cls.SCHEMA())  # pylint:disable=not-callable


class BaseOneOfSchema(Schema):
    """
    Code taken and adapted from: marshmallow-oneofschema

    This is a special kind of schema that actually multiplexes other schemas
    based on object type. When serializing values, it uses get_obj_type() method
    to get object type name. Then it uses `SCHEMAS` name-to-Schema mapping
    to get schema for that particular object type, serializes object using that
    schema and adds an extra "type" field with name of object type.
    Deserialization is reverse.
    """

    TYPE_FIELD = "type"
    TYPE_FIELD_REMOVE = True
    SCHEMAS = {}

    class Meta:
        unknown = RAISE

    def get_obj_type(self, obj):
        """Returns name of object schema"""
        return obj.IDENTIFIER or getattr(obj, self.TYPE_FIELD)

    def dump(self, obj, *, many=None):
        result_data = []
        result_errors = {}
        many = self.many if many is None else bool(many)
        if not many:
            result_data = self._dump(obj)
        else:
            for idx, o in enumerate(obj):
                try:
                    result = self._dump(o)
                    result_data.append(result)
                except ValidationError as error:
                    result_errors[idx] = error.messages
                    result_data.append(error.valid_data)

        result = result_data
        errors = result_errors

        if not errors:
            return result
        else:
            exc = ValidationError(errors, data=obj, valid_data=result)
            raise exc

    def _dump(self, obj):
        obj_type = self.get_obj_type(obj)
        if not obj_type:
            return (
                None,
                {"_schema": "Unknown object class: %s" % obj.__class__.__name__},
            )

        type_schema = self.SCHEMAS.get(obj_type)
        if not type_schema:
            return None, {"_schema": "Unsupported object type: %s" % obj_type}

        schema = type_schema if isinstance(type_schema, Schema) else type_schema()

        schema.context.update(getattr(self, "context", {}))

        result = schema.dump(obj, many=False)
        if result is not None:
            result[self.TYPE_FIELD] = obj_type
        return result

    def load(self, data, many=None, *, partial=None, unknown=None):
        result_data = []
        result_errors = {}
        many = self.many if many is None else bool(many)
        if partial is None:
            partial = self.partial
        if not many:
            try:
                result_data = self._load(data, partial=partial, unknown=unknown)
            except ValidationError as error:
                result_errors[0] = error.messages
                result_data.append(error.valid_data)
        else:
            for idx, item in enumerate(data):
                try:
                    result = self._load(item, partial=partial)
                    result_data.append(result)
                except ValidationError as error:
                    result_errors[idx] = error.messages
                    result_data.append(error.valid_data)

        result = result_data
        errors = result_errors

        if not errors:
            return result
        else:
            exc = ValidationError(errors, data=data, valid_data=result)
            raise exc

    def _load(self, data, partial=None, unknown=None):
        if not isinstance(data, dict):
            raise ValidationError({"_schema": "Invalid data type: %s" % data})

        data = dict(data)
        unknown = unknown or self.unknown

        data_type = data.get(self.TYPE_FIELD)
        if self.TYPE_FIELD in data and self.TYPE_FIELD_REMOVE:
            data.pop(self.TYPE_FIELD)

        if not data_type:
            raise ValidationError(
                {self.TYPE_FIELD: ["Missing data for required field."]}
            )

        try:
            type_schema = self.SCHEMAS.get(data_type)
        except TypeError:
            # data_type could be unhashable
            raise ValidationError({self.TYPE_FIELD: ["Invalid value: %s" % data_type]})
        if not type_schema:
            raise ValidationError(
                {self.TYPE_FIELD: ["Unsupported value: %s" % data_type]}
            )

        schema = type_schema if isinstance(type_schema, Schema) else type_schema()

        schema.context.update(getattr(self, "context", {}))

        return schema.load(data, many=False, partial=partial, unknown=unknown)

    def validate(self, data, *, many=None, partial=None):
        try:
            self.load(data, many=many, partial=partial)
        except ValidationError as ve:
            return ve.messages
        return {}


class BaseMultiSchema(Schema):
    __multi_schema_name__ = None
    __configs__ = None
    # to support snake case identifier, e.g. glorot_uniform and GlorotUniform
    __support_snake_case__ = False

    class Meta:
        unknown = EXCLUDE

    @post_dump(pass_original=True, pass_many=True)
    def handle_multi_schema_dump(self, data, pass_many, original):
        def handle_item(item):
            if hasattr(item, "get_config"):
                return self.__configs__[item.__class__.__name__].obj_to_schema(item)
            return item.to_schema()

        if pass_many:
            return [handle_item(item) for item in original]

        return handle_item(original)

    @post_load(pass_original=True, pass_many=True)
    def handle_multi_schema_load(self, data, pass_many, original):
        def make(key, val=None):
            key = to_camel_case(key) if self.__support_snake_case__ else key
            try:
                return (
                    self.__configs__[key].from_dict(val, unknown=EXCLUDE)
                    if val
                    else self.__configs__[key]()
                )
            except KeyError:
                raise ValidationError(
                    "`{}` is not a valid value for schema `{}`".format(
                        key, self.__multi_schema_name__
                    )
                )

        def handle_item(item):
            if isinstance(item, str):
                return make(item)

            if isinstance(item, Mapping):
                if "class_name" in item:
                    return make(item["class_name"], item["config"])
                if "model_type" in item:
                    return make(item.pop("model_type"), item)
                assert len(item) == 1
                key, val = list(item.items())[0]
                return make(key, val)

        if pass_many:
            return [handle_item(item) for item in original]

        return handle_item(original)


NAME_REGEX = r"^[-a-zA-Z0-9_]+\Z"
FULLY_QUALIFIED_NAME_REGEX = r"^[-a-zA-Z0-9_]+(:[-a-zA-Z0-9_.]+)?\Z"
