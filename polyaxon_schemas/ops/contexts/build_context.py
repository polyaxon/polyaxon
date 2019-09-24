# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import ValidationError, fields, validate, validates_schema

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.fields.docker_image import validate_image
from polyaxon_schemas.fields.ref_or_obj import RefOrObject


def validate_build_context_image(image):
    if not image:
        raise ValidationError("Invalid Build context, an image is required.")
    validate_image(image)


class BuildContextSchema(BaseSchema):
    context = fields.Str(allow_none=True)
    image = RefOrObject(fields.Str(allow_none=True))
    build_steps = RefOrObject(fields.List(fields.Str(), allow_none=True))
    lang_env = RefOrObject(fields.Str(allow_none=True))
    env_vars = RefOrObject(
        fields.List(
            fields.List(fields.Raw(), validate=validate.Length(equal=2)),
            allow_none=True,
        )
    )
    nocache = RefOrObject(fields.Boolean(allow_none=True))

    @staticmethod
    def schema_config():
        return BuildContextConfig

    @validates_schema
    def validate(self, data):
        validate_build_context_image(data.get("image"))


class BuildContextConfig(BaseConfig):
    IDENTIFIER = "build_context"
    SCHEMA = BuildContextSchema
    REDUCED_ATTRIBUTES = [
        "context",
        "image",
        "build_steps",
        "lang_env",
        "env_vars",
        "nocache",
    ]

    def __init__(
        self,
        context=None,
        image=None,
        build_steps=None,
        lang_env=None,
        env_vars=None,
        nocache=None,
    ):
        validate_build_context_image(image)
        self.context = context
        self.image = image
        self.build_steps = build_steps
        self.lang_env = lang_env
        self.env_vars = env_vars
        self.nocache = nocache

    @property
    def image_tag(self):
        if not self.image:
            return None
        tagged_image = self.image.split(":")
        if len(tagged_image) == 1:
            return "latest"
        if len(tagged_image) == 2:
            return "latest" if "/" in tagged_image[-1] else tagged_image[-1]
        if len(tagged_image) == 3:
            return tagged_image[-1]
