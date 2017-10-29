# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


class BaseObject(object):
    CONFIG = None

    @classmethod
    def from_config(cls, config):
        if not isinstance(config, cls.CONFIG):
            config = cls.CONFIG.from_dict(config)

        params = config.to_dict()
        params.pop('inbound_nodes', None)
        return cls(**params)

    def get_config(self):
        return self.CONFIG.obj_to_dict(self)
