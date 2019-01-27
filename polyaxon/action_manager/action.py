import logging

from typing import Any, Dict, List, Optional, Union

import auditor

from action_manager.exceptions import PolyaxonActionException
from event_manager.event import Event

logger = logging.getLogger("polyaxon.actions")

ConfigType = Union[Dict, List[Dict]]


class Action(object):
    action_key = None
    name = None
    description = ''
    event_type = None
    raise_empty_context = True
    check_config = True
    logger = logger

    @classmethod
    def _validate_config(cls, config: ConfigType) -> ConfigType:
        """Validate that a given config is valid for the current config."""
        raise NotImplementedError

    @classmethod
    def _get_config(cls) -> ConfigType:
        """Getting config to execute an action.

        Currently we get config from env vars.
        """
        raise NotImplementedError

    @classmethod
    def get_config(cls, config: ConfigType = None) -> ConfigType:
        config = config or cls._get_config()
        config = cls._validate_config(config)
        return config

    @classmethod
    def _prepare(cls, context: Dict) -> Dict:
        """This is where you should alter the context to fit the action.

        Default behaviour will leave the context as it is.
        """
        if not context and cls.raise_empty_context:
            raise PolyaxonActionException('{} received invalid payload context.'.format(cls.name))

        return context

    @classmethod
    def _execute(cls, data: Dict, config: Optional[ConfigType]) -> None:
        raise NotImplementedError

    @classmethod
    def serialize_event_to_context(cls, event: Event):
        """Implementation for turning an event into actionable notification."""
        pass

    @classmethod
    def execute(cls,
                context: Union[Dict, Event],
                config: Optional[ConfigType] = None,
                from_user: str = None,
                from_event: bool = False) -> Any:
        if from_event:
            context = cls.serialize_event_to_context(event=context)
            if not context:
                logger.warning('%s could not serializer event.', cls.name)
                return False

        config = cls.get_config(config=config)
        if cls.check_config and not config:
            return False

        data = cls._prepare(context)
        try:
            result = cls._execute(data=data, config=config)
            auditor.record(event_type=cls.event_type,
                           automatic=from_user is None,
                           user=from_user)
        except Exception:
            # Todo we need to show this somewhere in the dashboard
            logger.error('Exception during the execution of the action %s', cls, exc_info=True)
            return False
        return result
