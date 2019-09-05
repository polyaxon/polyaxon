# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from hestia.list_utils import to_list
from hestia.string_utils import strip_spaces
from marshmallow import ValidationError, fields, validates_schema

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.fields import ObjectOrListObject
from polyaxon_schemas.fields.docker_image import validate_image


def get_container_command_args(config):
    def sanitize_str(value):
        if not value:
            return
        value = strip_spaces(value=value, join=False)
        value = [c.strip().strip("\\") for c in value if (c and c != "\\")]
        value = [c for c in value if (c and c != "\\")]
        return " ".join(value)

    def sanitize(value):
        return (
            [sanitize_str(v) for v in value]
            if isinstance(value, list)
            else to_list(sanitize_str(value), check_none=True)
        )

    return to_list(config.command, check_none=True), sanitize(config.args)


def validate_container(image):
    if not image:
        raise ValidationError("The container section must contain an image.")


class ContainerSchema(BaseSchema):
    image = fields.Str()
    image_pull_policy = fields.Str(allow_none=True)
    command = ObjectOrListObject(fields.Str, allow_none=True)
    args = ObjectOrListObject(fields.Str, allow_none=True)

    @staticmethod
    def schema_config():
        return ContainerConfig

    @validates_schema
    def validate_container(self, values):
        validate_image(values.get("image"))
        validate_container(image=values.get("image"))


class ContainerConfig(BaseConfig):
    SCHEMA = ContainerSchema
    IDENTIFIER = "container"
    REDUCED_ATTRIBUTES = ["image_pull_policy", "command", "args"]

    def __init__(self, image, image_pull_policy=None, command=None, args=None):
        validate_image(image)
        validate_container(image=image)
        self.image = image
        self.image_pull_policy = image_pull_policy
        self.command = command
        self.args = args

    def get_container_command_args(self):
        return get_container_command_args(self)
