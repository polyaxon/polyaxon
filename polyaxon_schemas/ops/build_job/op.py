# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from marshmallow import ValidationError, fields, validate, validates_schema

from polyaxon_schemas.fields import IntOrStr
from polyaxon_schemas.ops.build_job.backends import BuildBackend
from polyaxon_schemas.ops.operation import BaseOpConfig, BaseOpSchema


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


def validate_build(**kwargs):
    if len([i for i in six.itervalues(kwargs) if i is not None and i != '']) != 1:
        raise ValidationError(
            'Invalid Build, only a a dockerfile, an image, or a reference is required.')


class BuildSchema(BaseOpSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal('build'))
    ref = IntOrStr(allow_none=True)
    backend = fields.Str(allow_none=True, validate=validate.OneOf(BuildBackend.VALUES))
    dockerfile = fields.Str(allow_none=True)
    context = fields.Str(allow_none=True)
    image = fields.Str(allow_none=True)
    build_steps = fields.List(fields.Str(), allow_none=True)
    lang_env = fields.Str(allow_none=True)
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
        validate_build(ref=data.get('ref'),
                       image=data.get('image'),
                       dockerfile=data.get('dockerfile'))


class BuildConfig(BaseOpConfig):
    SCHEMA = BuildSchema
    IDENTIFIER = 'build'
    REDUCED_ATTRIBUTES = BaseOpConfig.REDUCED_ATTRIBUTES + [
        'ref',
        'nocache',
        'branch',
        'build_steps',
        'env_vars',
        'lang_env',
        'commit',
        'backend',
        'context',
        'dockerfile',
        'image'
    ]

    def __init__(self,
                 version=None,
                 kind=None,
                 logging=None,
                 name=None,
                 description=None,
                 tags=None,
                 environment=None,
                 params=None,
                 inputs=None,
                 outputs=None,
                 ref=None,
                 dockerfile=None,
                 image=None,
                 context=None,
                 backend=None,
                 build_steps=None,
                 env_vars=None,
                 lang_env=None,
                 nocache=None,
                 commit=None,
                 branch=None):
        super(BuildConfig, self).__init__(
            version=version,
            kind=kind,
            logging=logging,
            name=name,
            description=description,
            tags=tags,
            environment=environment,
            params=params,
            inputs=inputs,
            outputs=outputs,
        )
        validate_image(image)
        validate_backend(backend)
        validate_build(ref=ref, image=image, dockerfile=dockerfile)
        self.ref = ref
        self.dockerfile = dockerfile
        self.context = context
        self.backend = backend
        self.image = image
        self.build_steps = build_steps
        self.env_vars = env_vars
        self.lang_env = lang_env
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
