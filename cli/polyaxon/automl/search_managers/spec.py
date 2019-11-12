import uuid

from collections import namedtuple


class SuggestionSpec(namedtuple("SuggestionSpec", "params")):
    """A structure that defines an experiment hyperparam suggestion."""

    def __eq__(self, other):
        if self.params.keys() != other.params.keys():
            return False

        for key, value in self.params.items():
            if value != other.params[key]:
                return False

        return True

    def __repr__(self):
        return ",".join(
            ["{}:{}".format(key, val) for (key, val) in sorted(self.params.items())]
        )

    def __hash__(self):
        return hash(self.__repr__())

    def uuid(self):
        return uuid.uuid5(uuid.NAMESPACE_DNS, self.__repr__())
