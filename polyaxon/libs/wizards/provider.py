class WizardProvider(object):
    """The base provider class implementing an interface for wizard views."""

    def get_wizard_views(self):
        """Returns a list of WizardView instance which will be dispatched in order.

        Example:
            >>> return [View1(), View2(), View3()]
        """
        raise NotImplementedError

    def set_config(self, config):
        """Used to allow additional provider configuration to be added to the provider instance."""
        self.config = config  # pylint:disbale=attribute-defined-outside-init
