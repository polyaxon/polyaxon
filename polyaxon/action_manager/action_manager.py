from libs.managers import ManagerInterface


class ActionManager(ManagerInterface):

    def _get_state_data(self, action):  # pylint:disable=arguments-differ
        return action.key, action

    def subscribe(self, action):  # pylint:disable=arguments-differ
        """
        >>> subscribe(SomeAction)
        """
        super().subscribe(obj=action)

    def knows(self, action):  # pylint:disable=arguments-differ
        return super().knows(key=action)

    def get(self, action):  # pylint:disable=arguments-differ
        return super().get(key=action)
