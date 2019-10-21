from marshmallow import fields

from schemas import BaseConfig, BaseSchema


class VolumeSchema(BaseSchema):
    existingClaim = fields.Str(allow_none=True)
    mountPath = fields.Str(allow_none=True)
    hostPath = fields.Str(allow_none=True)
    readOnly = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return VolumeConfig


class VolumeConfig(BaseConfig):
    SCHEMA = VolumeSchema
    IDENTIFIER = 'volume'

    def __init__(self, existingClaim=None, mountPath=None, hostPath=None, readOnly=False):  # noqa
        self.existingClaim = existingClaim
        self.mountPath = mountPath
        self.hostPath = hostPath
        self.readOnly = readOnly
