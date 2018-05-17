from libs.managers import ManagerInterface


class WizardManager(ManagerInterface):

    def _get_state_data(self, provider):
        return provider.key, provider

    def subscribe(self, provider):
        """
        >>> subscribe(SomeEvent)
        """
        super(WizardManager, self).subscribe(obj=provider)

    def knows(self, provider):
        return super(WizardManager, self).knows(key=provider)

    def get(self, provider):
        return super(WizardManager, self).get(key=provider)
