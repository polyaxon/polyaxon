# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields
from polyaxon_deploy.schemas.base import BaseConfig, BaseSchema


class IntegrationsSchema(BaseSchema):
    slack = fields.List(fields.Dict(), allow_none=True)
    hipchat = fields.List(fields.Dict(), allow_none=True)
    mattermost = fields.List(fields.Dict(), allow_none=True)
    discord = fields.List(fields.Dict(), allow_none=True)
    pagerduty = fields.List(fields.Dict(), allow_none=True)
    webhooks = fields.List(fields.Dict(), allow_none=True)

    @staticmethod
    def schema_config():
        return IntegrationsConfig


class IntegrationsConfig(BaseConfig):
    SCHEMA = IntegrationsSchema
    REDUCED_ATTRIBUTES = ['slack', 'hipchat', 'mattermost', 'discord', 'pagerduty', 'webhooks']

    def __init__(self,
                 slack=None,
                 hipchat=None,
                 mattermost=None,
                 discord=None,
                 pagerduty=None,
                 webhooks=None):
        self.slack = slack
        self.hipchat = hipchat
        self.mattermost = mattermost
        self.discord = discord
        self.pagerduty = pagerduty
        self.webhooks = webhooks
