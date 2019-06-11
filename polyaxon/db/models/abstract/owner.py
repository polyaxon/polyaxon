class OwnerMixin(object):

    @property
    def has_owner(self) -> bool:
        """Quick test to check the instance has an owner."""
        return bool(self.owner_id)
