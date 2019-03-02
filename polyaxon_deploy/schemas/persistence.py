# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from marshmallow import ValidationError, fields, validate, validates_schema
from polyaxon_deploy.schemas.base import BaseConfig, BaseSchema


def validate_persistence(existing_claim, host_path, store):
    if len([i for i in [existing_claim, host_path, store] if i]) > 1:
        raise ValidationError(
            'Only one of the option existingClaim, hostPath, and store '
            'can be used to define a persistence.')


class PersistenceEntitySchema(BaseSchema):
    existingClaim = fields.Str(allow_none=True)
    mountPath = fields.Str(allow_none=True)
    hostPath = fields.Str(allow_none=True)
    store = fields.Str(allow_none=True, validate=validate.OneOf(['s3', 'gcs', 'azure']))
    bucket = fields.Str(allow_none=True)
    secret = fields.Str(allow_none=True)
    secretKey = fields.Str(allow_none=True)
    readOnly = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return PersistenceEntityConfig

    @validates_schema
    def validate_persistence(self, data):
        existing_claim = data.get('existingClaim')
        host_path = data.get('hostPath')
        store = data.get('store')
        validate_persistence(existing_claim, host_path, store)


class PersistenceEntityConfig(BaseConfig):
    SCHEMA = PersistenceEntitySchema
    REDUCED_ATTRIBUTES = [
        'existingClaim',
        'mountPath',
        'hostPath',
        'store',
        'bucket',
        'secret',
        'secretKey',
        'readOnly'
    ]

    def __init__(self,  # noqa
                 existingClaim=None,
                 mountPath=None,
                 hostPath=None,
                 store=None,
                 bucket=None,
                 secret=None,
                 secretKey=None,
                 readOnly=None):
        validate_persistence(existingClaim, hostPath, store)
        self.existingClaim = existingClaim
        self.mountPath = mountPath
        self.hostPath = hostPath
        self.store = store
        self.bucket = bucket
        self.secret = secret
        self.secretKey = secretKey
        self.readOnly = readOnly


def validate_named_persistence(values, persistence):
    if not values:
        return
    for key, value in six.iteritems(values):
        try:
            PersistenceEntityConfig.from_dict(value)
        except (KeyError, ValidationError):
            raise ValidationError(
                "Persistence name `{}` under `{}` is not valid.".format(key, persistence))


class PersistenceSchema(BaseSchema):
    logs = fields.Nested(PersistenceEntitySchema, allow_none=True)
    repos = fields.Nested(PersistenceEntitySchema, allow_none=True)
    upload = fields.Nested(PersistenceEntitySchema, allow_none=True)
    data = fields.Dict(allow_none=True)
    outputs = fields.Dict(allow_none=True)

    @staticmethod
    def schema_config():
        return PersistenceConfig

    @validates_schema
    def validate_named_persistence(self, data):
        validate_named_persistence(data.get('data'), 'data')
        validate_named_persistence(data.get('outputs'), 'outputs')


class PersistenceConfig(BaseConfig):
    SCHEMA = PersistenceSchema
    REDUCED_ATTRIBUTES = ['logs', 'repos', 'upload', 'data', 'outputs']

    def __init__(self, logs=None, repos=None, upload=None, data=None, outputs=None):
        self.logs = logs
        self.repos = repos
        self.upload = upload
        if data:
            validate_named_persistence(data, 'data')
        self.data = data
        if outputs:
            validate_named_persistence(outputs, 'outputs')
        self.outputs = outputs
