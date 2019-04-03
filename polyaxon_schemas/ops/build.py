# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import ValidationError, fields, validate, validates_schema

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.ops.environments.base import EnvironmentSchema
from polyaxon_schemas.ops.logging import LoggingSchema
from polyaxon_schemas.utils import BuildBackend


def validate_image(image):
    if not image:
        return image
    if ' ' in image:
        raise ValidationError('Invalid docker image `{}`'.format(image))
    tagged_image = image.split(':')
    if len(tagged_image) > 3:
        raise ValidationError('Invalid docker image `{}`'.format(image))
    if len(tagged_image) == 3 and ('/' not in tagged_image[1] or tagged_image[1].startswith('/')):
        raise ValidationError('Invalid docker image `{}`'.format(image))


def validate_backend(backend):
    if backend and backend not in BuildBackend.VALUES:
        raise ValidationError('Build backend `{}` not supported'.format(backend))


def validate_build(image, dockerfile):
    build_data = [image, dockerfile]
    if all(build_data):
        raise ValidationError(
            'Invalid Build, only a dockerfile or image is required not both.'
            'received: image: `{}` and dockerfile: `{}`'.format(
                image,
                dockerfile
            ))
    if not any(build_data):
        raise ValidationError(
            'Invalid Build, a dockerfile or an image is required, received none.')


class BuildSchema(BaseSchema):
    version = fields.Int(allow_none=None)
    kind = fields.Str(allow_none=None, validate=validate.Equal('build'))
    logging = fields.Nested(LoggingSchema, allow_none=None)
    tags = fields.List(fields.Str(), allow_none=None)
    environment = fields.Nested(EnvironmentSchema, allow_none=True)
    backend = fields.Str(allow_none=True, validate=validate.OneOf(BuildBackend.VALUES))
    dockerfile = fields.Str(allow_none=True)
    context = fields.Str(allow_none=True)
    image = fields.Str(allow_none=True)
    build_steps = fields.List(fields.Str(), allow_none=True)
    env_vars = fields.List(fields.List(fields.Raw(), validate=validate.Length(equal=2)),
                           allow_none=True)
    commit = fields.Str(allow_none=True)
    branch = fields.Str(allow_none=True)
    nocache = fields.Boolean(allow_none=True)

    @staticmethod
    def schema_config():
        return BuildConfig

    @validates_schema
    def validate_image(self, data):
        """Validates docker image structure"""
        validate_image(data.get('image'))

    @validates_schema
    def validate_backend(self, data):
        """Validate backend"""
        validate_backend(data.get('backend'))

    @validates_schema
    def validate_config(self, data):
        validate_build(image=data.get('image'), dockerfile=data.get('dockerfile'))


class BuildConfig(BaseConfig):
    SCHEMA = BuildSchema
    IDENTIFIER = 'build'
    REDUCED_ATTRIBUTES = [
        'kind',
        'version',
        'logging',
        'tags',
        'environment',
        'build_steps',
        'env_vars',
        'nocache',
        'branch',
        'commit',
        'backend',
        'context',
        'dockerfile',
        'image'
    ]

    def __init__(self,
                 kind=None,
                 version=None,
                 logging=None,
                 tags=None,
                 environment=None,
                 dockerfile=None,
                 image=None,
                 context=None,
                 backend=None,
                 build_steps=None,
                 env_vars=None,
                 nocache=None,
                 commit=None,
                 branch=None):
        validate_image(image)
        validate_backend(backend)
        validate_build(image=image, dockerfile=dockerfile)
        self.kind = kind
        self.version = version
        self.logging = logging
        self.tags = tags
        self.environment = environment
        self.dockerfile = dockerfile
        self.context = context
        self.backend = backend
        self.image = image
        self.build_steps = build_steps
        self.env_vars = env_vars
        self.nocache = nocache
        self.commit = commit
        self.branch = branch

    @property
    def image_tag(self):
        if not self.image:
            return None
        tagged_image = self.image.split(':')
        if len(tagged_image) == 1:
            return 'latest'
        if len(tagged_image) == 2:
            return 'latest' if '/' in tagged_image[-1] else tagged_image[-1]
        if len(tagged_image) == 3:
            return tagged_image[-1]
