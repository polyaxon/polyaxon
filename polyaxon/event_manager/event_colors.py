from typing import Any

from constants.statuses import StatusOptions
from event_manager import event_actions, event_context


class EventColor(object):
    GREEN = '#1aaa55'
    RED = '#aa310f'
    BLUE = '#2e77aa'
    YELLOW = '#aa9e4a'
    GREY = '#485563'

    @classmethod
    def get_for_event(cls, event_content_object: Any, event_type: str) -> str:
        action = event_context.get_event_action(event_type=event_type)
        if action in [event_actions.FAILED,
                      event_actions.STOPPED,
                      event_actions.DELETED]:
            return cls.RED
        if action in [event_actions.SUCCEEDED]:
            return cls.GREEN

        if action != event_actions.NEW_STATUS:
            return cls.GREY

        if event_content_object.last_status in [StatusOptions.FINISHED, StatusOptions.SKIPPED]:
            return cls.GREEN

        if event_content_object.last_status == StatusOptions.DONE:
            return cls.GREY

        if event_content_object.last_status == StatusOptions.CREATED:
            return cls.BLUE

        return cls.YELLOW
