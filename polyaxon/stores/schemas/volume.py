from marshmallow import Schema, fields, post_dump, post_load

from schemas.base import BaseConfig


class VolumeSchema(Schema):
    existingClaim = fields.Str(allow_none=True)
    mountPath = fields.Str(allow_none=True)
    hostPath = fields.Str(allow_none=True)
    readOnly = fields.Bool(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return VolumeConfig(**data)

    @post_dump
    def unmake(self, data):
        return VolumeConfig.remove_reduced_attrs(data)


class VolumeConfig(BaseConfig):
    SCHEMA = VolumeSchema
    IDENTIFIER = 'volume'

    def __init__(self, existingClaim=None, mountPath=None, hostPath=None, readOnly=False):
        self.existingClaim = existingClaim
        self.mountPath = mountPath
        self.hostPath = hostPath
        self.readOnly = readOnly
