from collections import namedtuple


class RegistryContextSpec(namedtuple("RegistryContextSpec", "host secret secret_items insecure")):

    def items(self):
        return self._asdict().items()
