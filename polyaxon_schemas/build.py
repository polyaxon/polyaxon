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
    if len(tagged_image) > 3:
        raise ValidationError('Invalid docker image `{}`'.format(image))
    if len(tagged_image) == 3 and ('/' not in tagged_image[1] or tagged_image[1].startswith('/')):
        raise ValidationError('Invalid docker image `{}`'.format(image))


class BuildSchema(Schema):
    image = fields.Str()
    build_steps = fields.List(fields.Str(), allow_none=True)
    env_vars = fields.List(fields.List(fields.Raw(), validate=validate.Length(equal=2)),
                           allow_none=True)
    git = fields.Str(allow_none=True)
    ref = fields.Str(allow_none=True)
    nocache = fields.Boolean(allow_none=True)

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
    """
    Build config.

    Args:
        image: str. The name of the image to use during the build step.
        build_steps: list(str). The build steps to apply to your docker image.
            (translate to multiple RUN ...)
        env_vars: list((str, str)) The environment variable to set on you docker image.
        nocache: `bool`. To not use cache when building the image.
        git: `str`. A url to git code, in case you are not using upload.
        ref: `str`. The commit/branch/treeish to use.

    """
    SCHEMA = BuildSchema
    IDENTIFIER = 'build'
    REDUCED_ATTRIBUTES = ['build_steps', 'env_vars', 'git', 'nocache', 'ref']

    def __init__(self, image, build_steps=None, env_vars=None, nocache=None, git=None, ref=None):
        validate_image(image)
        self.image = image
        self.build_steps = build_steps
        self.env_vars = env_vars
        self.git = git
        self.nocache = nocache
        self.ref = ref

    @property
    def image_tag(self):
        tagged_image = self.image.split(':')
        if len(tagged_image) == 1:
            return 'latest'
        if len(tagged_image) == 2:
            return 'latest' if '/' in tagged_image[-1] else tagged_image[-1]
        if len(tagged_image) == 3:
            return tagged_image[-1]
