from libs.managers import ManagerInterface


class WizardManager(ManagerInterface):

    def _get_state_data(self, provider):  # pylint:disable=arguments-differ
        return provider.key, provider

    def subscribe(self, provider):  # pylint:disable=arguments-differ
        """
        >>> subscribe(SomeEvent)
        """
        super(WizardManager, self).subscribe(obj=provider)

    def knows(self, provider):  # pylint:disable=arguments-differ
        return super(WizardManager, self).knows(key=provider)

    def get(self, provider):  # pylint:disable=arguments-differ
        return super(WizardManager, self).get(key=provider)
