import logging

import auditor

logger = logging.getLogger("polyaxon.actions")


class Action(object):
    action_key = None
    name = None
    description = ''
    event_type = None

    @classmethod
    def _get_config(cls):
        """Getting config to be execute an action.

        Currently we get config from env vars.
        """
        raise NotImplementedError

    @classmethod
    def get_config(cls, config=None):
        if config:
            return config
        return cls._get_config()

    @classmethod
    def _prepare(cls, context):
        """This is where you should alter the context to fit the action.

        Default behaviour will leave the context as it is.
        """
        return context

    @classmethod
    def _execute(cls, data, config):
        raise NotImplementedError

    @classmethod
    def execute(cls, context, config=None, from_user=None):
        config = cls.get_config(config=config)
        data = cls._prepare(context)
        result = cls._execute(data=data, config=config)
        auditor.record(event_type=cls.event_type,
                       automatic=from_user is None,
                       user=from_user)
        return result
