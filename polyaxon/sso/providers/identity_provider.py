from libs.wizards import WizardProvider


class IdentityProvider(WizardProvider):
    """The `identityBuilder` class provides a wizard provider to construct an identity."""

    def __init__(self, **kwargs):
        self.config = kwargs

    def build_identity(self, state_data):
        """Return a mapping containing the identity information.

        The resulting data captured by the pipeline

            >>> {
            >>>     "id":     "foo@example.com",
            >>>     "email":  "foo@example.com",
            >>>     "name":   "Foo Bar",
            >>>     "scopes": ['emaill', ...],
            >>>     "data":   { ... },
            >>> }


        Raises:
             InvalidIdentity
        """
        raise NotImplementedError

    def update_identity(self, new_data, current_data):
        """Return the new state which should be used for an identity."""
        return new_data

    def refresh_identity(self, auth_identity):
        """Refresh identity from upstream.

        Raises:
             InvalidIdentity
        """
        raise NotImplementedError
