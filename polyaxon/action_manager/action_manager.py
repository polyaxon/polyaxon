from typing import Tuple

from hestia.manager_interface import ManagerInterface

from action_manager.action import Action


class ActionManager(ManagerInterface):

    def _get_state_data(self,  # pylint:disable=arguments-differ
                        action: Action) -> Tuple[str, Action]:
        return action.action_key, action

    def subscribe(self, action: Action) -> None:  # pylint:disable=arguments-differ
        """
        >>> subscribe(SomeAction)
        """
        super().subscribe(obj=action)

    def knows(self, action_key: str) -> bool:  # pylint:disable=arguments-differ
        return super().knows(key=action_key)

    def get(self, action_key: str) -> Action:  # pylint:disable=arguments-differ
        return super().get(key=action_key)
