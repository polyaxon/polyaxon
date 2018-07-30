from libs.managers import ManagerInterface


class ActionManager(ManagerInterface):

    def _get_state_data(self, action):  # pylint:disable=arguments-differ
        return action.key, action

    def subscribe(self, action):  # pylint:disable=arguments-differ
        """
        >>> subscribe(SomeAction)
        """
        super().subscribe(obj=action)

    def knows(self, action_key):  # pylint:disable=arguments-differ
        return super().knows(key=action_key)

    def get(self, action_key):  # pylint:disable=arguments-differ
        return super().get(key=action_key)
