class UniqueNameMixin(object):
    """
    A mixin to force setting a unique name.
    """

    @property
    def unique_name(self) -> str:
        raise NotImplementedError()
