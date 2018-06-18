# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import (
    Schema,
    ValidationError,
    fields,
    post_dump,
    post_load,
    validate,
    validates_schema
)

from polyaxon_schemas.base import BaseConfig


def validate_image(image):
    if not image:
        raise ValidationError('Invalid docker image `{}`'.format(image))
    tagged_image = image.split(':')
    if len(tagged_image) > 2:
        raise ValidationError('Invalid docker image `{}`'.format(image))


class BuildSchema(Schema):
    image = fields.Str()
    build_steps = fields.List(fields.Str(), allow_none=True)
    env_vars = fields.List(fields.List(fields.Raw(), validate=validate.Length(equal=2)),
                           allow_none=True)
    git = fields.Str(allow_none=True)
    nocache = fields.Boolean(allow_none=True)
    commit = fields.Str(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return BuildConfig(**data)

    @post_dump
    def unmake(self, data):
        return BuildConfig.remove_reduced_attrs(data)

    @validates_schema
    def validate_image(self, data):
        """Validates docker image structure"""
        validate_image(data.get('image'))


class BuildConfig(BaseConfig):
    SCHEMA = BuildSchema
    IDENTIFIER = 'build'
    REDUCED_ATTRIBUTES = ['build_steps', 'env_vars', 'git', 'nocache', 'commit']

    def __init__(self, image, build_steps=None, env_vars=None, git=None, nocache=None, commit=None):
        validate_image(image)
        self.image = image
        self.build_steps = build_steps
        self.env_vars = env_vars
        self.git = git
        self.nocache = nocache
        self.commit = commit

    @property
    def image_tag(self):
        tagged_image = self.image.split(':')
        if len(tagged_image) == 1:
            return 'latest'

        return tagged_image[1]
