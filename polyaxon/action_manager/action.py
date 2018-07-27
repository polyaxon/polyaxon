import logging

import auditor

logger = logging.getLogger("polyaxon.actions")


class Action(object):
    key = None
    name = None
    description = ''
    event_type = None

    def _get_config(self):
        """Getting config to be execute an action.

        Currently we get config from env vars.
        """
        raise NotImplementedError

    def get_config(self, config=None):
        if config:
            return config
        return self._get_config()

    def _prepare(self, context):
        """This is where you should alter the context to fit the action.

        Default behaviour will leave the context as it is.
        """
        return context

    def _execute(self, data, config):
        raise NotImplementedError

    def execute(self, context, config=None, from_user=None):
        config = self.get_config(config=config)
        data = self._prepare(context)
        resutl = self._execute(data=data, config=config)
        auditor.record(event_type=self.event_type,
                       automatic=from_user is None,
                       user=from_user)
        return resutl
