from marshmallow import ValidationError, fields, validates_schema

from constants import stores
from schemas.base import BaseConfig, BaseSchema


def validate_store(store):
    if store not in stores.VALUES:
        raise ValidationError("Store is not valid.")


class StoreSchema(BaseSchema):
    store = fields.Str()
    bucket = fields.Str()
    secret = fields.Str()
    secretKey = fields.Str()

    @staticmethod
    def schema_config():
        return StoreConfig

    @validates_schema
    def validate_store(self, data):
        if data.get('store'):
            validate_store(data['pvalues'])


class StoreConfig(BaseConfig):
    SCHEMA = StoreSchema
    IDENTIFIER = 'store'

    def __init__(self, store, bucket, secret, secretKey):  # noqa
        self.store = store
        self.bucket = bucket
        self.secret = secret
        self.secretKey = secretKey
